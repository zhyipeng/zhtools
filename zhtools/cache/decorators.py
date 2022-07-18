import asyncio
import inspect
from typing import Any

import wrapt

from zhtools.cache.storages import Empty, MemoryStorage
from zhtools.config import config
from zhtools.type_hint import MakeCacheKeyFunc, Wrapped

storage = MemoryStorage()


def is_async(func: Wrapped):
    if isinstance(func, classmethod):
        func = func.__wrapped__
    return inspect.iscoroutinefunction(func)


def get_func_name(func: Wrapped) -> str:
    if inspect.isfunction(func) or inspect.ismethod(func):
        return func.__name__
    return func.__class__.__name__


def make_cache_key(func: Wrapped, *args, **kwargs) -> str:
    return f'{get_func_name(func)}:{(args, kwargs)}'


class cache:

    def __new__(cls,
                func: Wrapped = None,
                /,
                key: MakeCacheKeyFunc = make_cache_key):
        obj = super().__new__(cls)
        cls.__init__(obj, key=key)
        if func is not None:
            obj = obj.__call__(func)
        return obj

    def __init__(self, key: MakeCacheKeyFunc = make_cache_key):
        self.key = key

    def get_cache_key(self, func: Wrapped, instance: Any, args, kwargs) -> str:
        if instance is not None and not inspect.isclass(instance):
            return self.key(func, instance, *args, **kwargs)
        else:
            return self.key(func, *args, **kwargs)

    @wrapt.decorator
    def wrapper(self, func: Wrapped, instance: Any, args, kwargs) -> Wrapped:
        cache_key = self.get_cache_key(func, instance, args, kwargs)
        cache_result = config.storage.get(cache_key)
        if cache_result is not Empty:
            return cache_result

        result = func(*args, **kwargs)

        config.storage.setex(cache_key, result, config.default_expire)
        return result

    @wrapt.decorator
    async def async_wrapper(self, func: Wrapped, instance: Any, args, kwargs) -> Wrapped:
        cache_key = self.get_cache_key(func, instance, args, kwargs)
        cache_result = await config.storage.get(cache_key)
        if cache_result is not Empty:
            return cache_result

        result = await func(*args, **kwargs)

        asyncio.create_task(
            config.storage.setex(cache_key, result, config.default_expire)
        )
        return result

    def __call__(self, func: Wrapped):
        if is_async(func):
            return self.async_wrapper(func)
        return self.wrapper(func)