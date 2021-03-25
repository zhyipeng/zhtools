import abc
import os
import pickle
import time
import shelve
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

    def _get(self, key: AnyStr) -> Any:
        return self.__storage.get(key)

    def _set(self,
             key: AnyStr,
             value: AnyStr,
             expire: Optional[int] = None) -> None:
        self.__storage[key] = value

    def _delete(self, key: AnyStr) -> None:
        self.__storage.pop(key, None)

    def get(self, key: AnyStr) -> Any:
        expire = self.__expires.get(key)
        if expire and expire >= time.time():
            self.delete(key)
            return None
        return self._get(key)

    def set(self, key: AnyStr, value: AnyStr,
            expire: Optional[int] = None) -> None:
        self._set(key, value, expire)
        if expire is not None:
            self.__expires[key] = time.time() + expire

    def delete(self, key: AnyStr) -> None:
        self._delete(key)
        self.__expires.pop(key, None)


class FileCacheStorage(MemoryCacheStorage):
    """Cache storage use file"""

    def __init__(self, path: str = '/tmp'):
        super().__init__()
        self.path = path

    def _get(self, key: AnyStr) -> Any:
        with open(os.path.join(self.path, str(key)), 'rb') as f:
            return pickle.load(f)

    def _set(self,
             key: AnyStr,
             value: Any,
             expire: Optional[int] = None) -> None:
        with open(os.path.join(self.path, str(key)), 'wb') as f:
            pickle.dump(value, f)

    def _delete(self, key: AnyStr) -> None:
        os.remove(os.path.join(self.path, key))


class ShelveCacheStorage(MemoryCacheStorage):

    def __init__(self, db: str = 'shelve_cache'):
        super().__init__()
        self.db = db

    def _set(self,
             key: AnyStr,
             value: AnyStr,
             expire: Optional[int] = None) -> None:
        with shelve.open(self.db) as db:
            db[key] = value

    def _get(self, key: AnyStr) -> Any:
        with shelve.open(self.db) as db:
            return db.get(key)

    def _delete(self, key: AnyStr) -> None:
        with shelve.open(self.db) as db:
            db.pop(key, None)
