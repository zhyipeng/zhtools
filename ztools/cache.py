import abc
import functools
import inspect
import pickle
import time
from typing import Any, Callable, Optional, Union, AnyStr

from ztools.utils import uuid4_hex


def default_get_key_suffix(*args, **kwargs):
    r = {'args': args, 'kwargs': kwargs}
    return pickle.dumps(r)


def make_cache_key(key_prefix: str,
                   key_suffix: Union[Callable, str],
                   *args,
                   **kwargs) -> str:
    if inspect.isfunction(key_suffix):
        suffix = key_suffix(*args, **kwargs)
    else:
        suffix = key_suffix

    return f'{key_prefix}:{suffix}'


class CacheStorageInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, key: AnyStr) -> Any:
        pass

    @abc.abstractmethod
    def set(self,
            key: AnyStr,
            value: AnyStr,
            expire: Optional[int] = None) -> None:
        pass

    @abc.abstractmethod
    def delete(self, key: AnyStr) -> None:
        pass


class MemoryCacheStorage(CacheStorageInterface):

    def __init__(self):
        self.__storage = {}
        self.__expires = {}

    def get(self, key: AnyStr) -> Any:
        expire = self.__expires.get(key)
        if expire and expire >= time.time():
            self.__storage.pop(key, None)
            return None
        return self.__storage.get(key)

    def set(self, key: AnyStr, value: AnyStr,
            expire: Optional[int] = None) -> None:
        self.__storage[key] = value
        if expire is not None:
            self.__expires[key] = time.time() + expire

    def delete(self, key: AnyStr) -> None:
        self.__storage.pop(key, None)
        self.__expires.pop(key, None)


class Cache:
    storage: CacheStorageInterface = MemoryCacheStorage

    def __init__(self,
                 key_prefix: str = '',
                 key_suffix: Union[Callable, str] = default_get_key_suffix,
                 cache_expires: Optional[int] = None,
                 ignore_exception: bool = False):
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
                if self.ignore_exception:
                    raise r
                else:
                    return

            return r

    def __call__(self, func: Callable):

        def wrapped(*args, **kwargs):
            key = self.make_cache_key(*args, **kwargs)
            result = self.get_cached_result(key)
            if not result:
                result = func(*args, **kwargs)
                self.storage.set(key, result, self.cache_expires)
            return result

        def update_cached_result(result: Any, *args, **kwargs):
            key = self.make_cache_key(*args, **kwargs)
            if result is None:
                self.storage.delete(key)
            else:
                self.storage.set(key, result, self.cache_expires)

        functools.update_wrapper(wrapped, func)
        wrapped.update_cached_result = update_cached_result
        return wrapped
