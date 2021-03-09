import abc
import os
import pickle
import time
from typing import Any, AnyStr, Optional


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
    """Cache storage use memory"""

    def __init__(self):
        self.__storage = {}
        self.__expires = {}

    def get(self, key: AnyStr) -> Any:
        expire = self.__expires.get(key)
        if expire and expire >= time.time():
            self.delete(key)
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


class FileCacheStorage(CacheStorageInterface):
    """Cache storage use file"""

    def __init__(self, path: str = '/tmp'):
        self.path = path
        self.__expires = {}

    def read_file(self, key: AnyStr) -> Any:
        with open(os.path.join(self.path, str(key)), 'rb') as f:
            return pickle.load(f)

    def save_file(self, key: AnyStr, data: Any) -> None:
        with open(os.path.join(self.path, str(key)), 'wb') as f:
            pickle.dump(data, f)

    def get(self, key: AnyStr) -> Any:
        expire = self.__expires.get(key)
        if expire and expire >= time.time():
            self.delete(key)
            return None

        return self.read_file(key)

    def set(self,
            key: AnyStr,
            value: AnyStr,
            expire: Optional[int] = None) -> None:
        self.save_file(key, value)
        if expire is not None:
            self.__expires[key] = time.time() + expire

    def delete(self, key: AnyStr) -> None:
        self.__expires.pop(key, None)
        os.remove(os.path.join(self.path, key))

