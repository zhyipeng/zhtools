import functools
import inspect
import pickle
from typing import Any, Callable, Optional, Union

from zhtools.cache.storages import CacheStorageInterface, MemoryCacheStorage
from zhtools.random import uuid4_hex


def default_get_key_suffix(*args, **kwargs):
    """Generate cache key suffix from function parameters."""
    r = {'args': args, 'kwargs': kwargs}
    return pickle.dumps(r)


def make_cache_key(key_prefix: str,
                   key_suffix: Union[Callable, str],
                   *args,
                   **kwargs) -> str:
    """Generate cache key from function parameters"""
    if inspect.isfunction(key_suffix):
        suffix = key_suffix(*args, **kwargs)
    else:
        suffix = key_suffix

    return f'{key_prefix}:{suffix}'


class Cache:
    """
    Cache tool
    >>> @Cache(key_prefix='cache_key')
    >>> def foo():
    >>>     return True

    storage: cache storage, default storage is use by memory.
    """
    storage: CacheStorageInterface = MemoryCacheStorage()

    def __init__(self,
                 key_prefix: str = '',
                 key_suffix: Union[Callable, str] = default_get_key_suffix,
                 cache_expires: Optional[int] = None,
                 ignore_exception: bool = True):
        """
        :param key_prefix: the prefix of cache key
        :param key_suffix: the suffix of cache key
        :param cache_expires: the expires of cache, seconds
        :param ignore_exception: while is True, it will skip cache when
                                 function raised exception
        """
        self.key_prefix = key_prefix
        self.key_suffix = key_suffix
        self.cache_expires = cache_expires
        self.name = uuid4_hex()
        self.ignore_exception = ignore_exception

    def make_cache_key(self, *args, **kwargs):
        return make_cache_key(self.key_prefix, self.key_suffix, *args, **kwargs)

    def get_cached_result(self, key: str) -> Any:
        r = self.storage.get(key)
        if not r:
            return

        if not isinstance(r, bytes):
            return r

        r = pickle.loads(r)
        if r:
            if isinstance(r, Exception):
                raise r

            return r

    def __call__(self, func: Callable):

        def wrapped(*args, **kwargs):
            key = self.make_cache_key(*args, **kwargs)
            result = self.get_cached_result(key)
            if not result:
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    if self.ignore_exception:
                        raise e

                    result = e
                self.storage.set(key, result, self.cache_expires)

            if isinstance(result, Exception):
                raise result
            return result

        def update_cached_result(result: Any, *args, **kwargs) -> None:
            """
            method to update cache
            >>> @Cache()
            >>> def foo():
            >>>    return 1
            >>> foo.update_cached_result(0)
            >>> foo()
                0

            :param result: cache value
            :param args: args for making cache key
            :param kwargs: kwargs for making cache key
            """
            key = self.make_cache_key(*args, **kwargs)
            if result is None:
                self.storage.delete(key)
            else:
                self.storage.set(key, result, self.cache_expires)

        functools.update_wrapper(wrapped, func)
        wrapped.update_cached_result = update_cached_result
        return wrapped


cache = Cache
