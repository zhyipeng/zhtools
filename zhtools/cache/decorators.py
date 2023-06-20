import asyncio
import functools
import inspect
from collections.abc import Callable
from typing import Any, AnyStr, overload

import wrapt

from zhtools.config import config
from zhtools.typing import (AsyncWrapped, AsyncWrapper, CommonWrapped,
                            CommonWrapper, P)
from .storages import Empty


def _is_async(func: Callable):
    if isinstance(func, classmethod):
        func = func.__wrapped__
    return inspect.iscoroutinefunction(func)


MakeCacheKeyFunc = Callable[[CommonWrapped, P], AnyStr]


def get_func_name(func: Callable) -> str:
    if inspect.isfunction(func) or inspect.ismethod(func):
        return func.__name__
    return func.__class__.__name__


def make_cache_key(func: CommonWrapped, *args, **kwargs) -> str:
    return f'{get_func_name(func)}:{(args, kwargs)}'


class cache:
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

    def __new__(cls,
                func: CommonWrapped = None,
                *,
                key: MakeCacheKeyFunc = make_cache_key,
                expire: int = None):
        obj = super().__new__(cls)
        cls.__init__(obj, key=key)
        if func is not None and (callable(func) or isinstance(func, classmethod)):
            obj = obj.__call__(func)

        return obj

    def __init__(self, *, key: MakeCacheKeyFunc = make_cache_key, expire: int = None):
        self.key = key
        self.expire = expire or config.default_expire

    def get_key(self, func: CommonWrapped, instance: Any, args: P.args, kwargs: P.kwargs) -> str:
        if instance is not None and not inspect.isclass(instance):
            return self.key(func, instance, *args, **kwargs)
        else:
            return self.key(func, *args, **kwargs)

    @wrapt.decorator
    def wrapper(self, func: CommonWrapped, instance: Any, args: P.args, kwargs: P.kwargs) -> CommonWrapper:
        _key = self.get_key(func, instance, args, kwargs)
        cache_result = config.storage.get(_key)
        if cache_result is not Empty:
            return cache_result

        result = func(*args, **kwargs)
        config.storage.setex(_key, result, self.expire)
        return result

    @wrapt.decorator
    async def async_wrapper(self,
                            func: AsyncWrapped,
                            instance: Any,
                            args: P.args,
                            kwargs: P.kwargs) -> AsyncWrapper:
        _key = self.get_key(func, instance, args, kwargs)
        cache_result = await config.storage.get(_key)
        if cache_result is not Empty:
            return cache_result

        result = await func(*args, **kwargs)
        asyncio.create_task(config.storage.setex(_key, result, self.expire))
        return result

    @overload
    def __call__(self, func: AsyncWrapped) -> AsyncWrapper:
        ...

    def __call__(self, func: CommonWrapped) -> CommonWrapper:
        if _is_async(func):
            return self.async_wrapper(func)
        return self.wrapper(func)


class cond_lru_cache:
    """use functools.lru_cache when use_cache return True"""

    def __init__(self,
                 use_cache: Callable[P, bool],
                 maxsize: int = 128,
                 typed: bool = False):
        self.use_cache = use_cache
        self.maxsize = maxsize
        self.typed = typed

    @wrapt.decorator
    def __call__(self,
                 func: CommonWrapped,
                 instance: Any,
                 args: P.args,
                 kwargs: P.kwargs) -> CommonWrapper:
        deco_func = functools.lru_cache(self.maxsize, self.typed)(func)
        if self.use_cache(*args, **kwargs):
            return deco_func(*args, **kwargs)

        return func(*args, **kwargs)
