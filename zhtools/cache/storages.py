import abc
import time
from typing import Any

Empty = object()


class Storage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        pass

    def set(self, key: str, value: Any):
        self.setex(key, value, float('inf'))

    @abc.abstractmethod
    def setex(self, key: str, value: Any, expire: float):
        pass


class AsyncStorage(Storage, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def get(self, key: str) -> Any:
        pass

    async def set(self, key: str, value: Any):
        await self.setex(key, value, float('inf'))

    @abc.abstractmethod
    async def setex(self, key: str, value: Any, expire: float):
        pass


class MemoryStorage(Storage):

    def __init__(self):
        self.data: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any:
        val, expire = self.data.get(key, (Empty, 0))
        if val is Empty:
            return val

        if expire < time.time():
            del self.data[key]
            return Empty
        return val

    def setex(self, key: str, value: Any, expire: float):
        if expire is None:
            expire = float('inf')
        expire_at = time.time() + expire
        self.data[key] = (value, expire_at)
