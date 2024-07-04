import asyncio
import functools
import inspect
from collections.abc import Callable
from typing import Any, Protocol, Self, overload

import wrapt

from zhtools.config import config
from zhtools.typing import CommonWrapped, CommonWrapper

from .storages import Empty


def _is_async(func: Callable):
    if isinstance(func, classmethod):
        func = func.__wrapped__
    return inspect.iscoroutinefunction(func)


def get_func_name(func: Callable) -> str:
    if inspect.isfunction(func) or inspect.ismethod(func):
        return func.__name__
    return func.__class__.__name__


class cache[T, **P]:
    """
    >>> from zhtools.cache.storages import RedisStorage
    >>> config.storage = RedisStorage()
    >>> @cache
    >>> def foo(a: int, b: int) -> int:
    ...
    >>> @cache(key=lambda a, b: f'{a}:{b}')
    >>> def foo1(a: int, b: int) -> int:
    ...
    """

    class MakeCacheKeyFunc(Protocol):
        def __call__(
            self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs
        ) -> str: ...

    @staticmethod
    def default_make_cache_key(func: Callable[P, T], *args, **kwargs):
        return f"{get_func_name(func)}:{(args, kwargs)}"

    @overload
    def __new__(cls) -> Self: ...

    @overload
    def __new__(
        cls,
        func: Callable[P, T],
        *,
        key: MakeCacheKeyFunc = default_make_cache_key,
        expire: int | None = None,
    ) -> Callable[P, T]: ...

    def __new__(
        cls,
        func: Callable[P, T] | None = None,
        *,
        key: MakeCacheKeyFunc = default_make_cache_key,
        expire: int | None = None,
    ) -> Callable[P, T] | Self:
        obj: Self = super().__new__(cls)
        cls.__init__(obj, key=key)
        if func is not None and (callable(func) or isinstance(func, classmethod)):
            return obj.__call__(func)

        return obj

    def __init__(
        self,
        *,
        key: MakeCacheKeyFunc = default_make_cache_key,
        expire: int | None = None,
    ):
        self.key = key
        self.expire: int = expire or config.default_expire or 0

    def get_key(self, func: Callable[P, T], instance: Any, args, kwargs) -> str:
        if instance is not None and not inspect.isclass(instance):
            return self.key(func, instance, *args, **kwargs)
        else:
            return self.key(func, *args, **kwargs)

    @wrapt.decorator
    def wrapper(
        self,
        func: Callable[P, T],
        instance: Any,
        args,
        kwargs,
    ) -> Callable[P, T]:
        _key = self.get_key(func, instance, args, kwargs)
        cache_result = config.storage.get(_key)
        if cache_result is not Empty:
            return cache_result

        result = func(*args, **kwargs)  # type: ignore
        config.storage.setex(_key, result, self.expire)
        return result  # type: ignore

    @wrapt.decorator
    async def async_wrapper(
        self, func: Callable[P, T], instance: Any, args, kwargs
    ) -> Callable[P, T]:
        _key = self.get_key(func, instance, args, kwargs)
        cache_result = await config.storage.get(_key)
        if cache_result is not Empty:
            return cache_result

        result = await func(*args, **kwargs)  # type: ignore
        asyncio.create_task(config.storage.setex(_key, result, self.expire))  # type: ignore
        return result

    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        if _is_async(func):
            return self.async_wrapper(func)  # type: ignore
        return self.wrapper(func)  # type: ignore


class cond_lru_cache:
    """use functools.lru_cache when use_cache return True"""

    def __init__(
        self, use_cache: Callable[..., bool], maxsize: int = 128, typed: bool = False
    ):
        self.use_cache = use_cache
        self.maxsize = maxsize
        self.typed = typed

    @wrapt.decorator
    def __call__(
        self,
        func: CommonWrapped,
        instance: Any,
        args,
        kwargs,
    ) -> CommonWrapper:
        deco_func = functools.lru_cache(self.maxsize, self.typed)(func)
        if self.use_cache(*args, **kwargs):
            return deco_func(*args, **kwargs)

        return func(*args, **kwargs)
