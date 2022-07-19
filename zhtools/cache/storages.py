import abc
import logging
import pickle
import time
import typing
from typing import Any

if typing.TYPE_CHECKING:
    from redis import Redis
    from aioredis import Redis as AsyncRedis

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


class RedisStorage(Storage):

    def __init__(self, redis_cli: 'Redis'):
        self.redis_cli = redis_cli

    def get(self, key: str) -> Any:
        ret = self.redis_cli.get(key)
        if ret is None:
            return Empty

        if isinstance(ret, bytes):
            try:
                ret = pickle.loads(ret)
            except pickle.UnpicklingError:
                pass

        return ret

    def setex(self, key: str, value: Any, expire: float):
        try:
            value = pickle.dumps(value)
        except pickle.PickleError:
            logging.error(f'cache value {value} can not pickle.')
            return

        if expire is None or expire == float('inf'):
            self.redis_cli.set(key, value)
        else:
            self.redis_cli.setex(key, int(expire), value)


class AsyncRedisStorage(AsyncStorage):

    def __init__(self, redis_cli: 'AsyncRedis'):
        self.redis_cli = redis_cli

    async def get(self, key: str) -> Any:
        ret = await self.redis_cli.get(key)
        if ret is None:
            return Empty

        if isinstance(ret, bytes):
            try:
                ret = pickle.loads(ret)
            except pickle.UnpicklingError:
                pass

        return ret

    async def setex(self, key: str, value: Any, expire: float):
        try:
            value = pickle.dumps(value)
        except pickle.PickleError:
            logging.error(f'cache value {value} can not pickle.')
            return

        if expire is None or expire == float('inf'):
            await self.redis_cli.set(key, value)
        else:
            await self.redis_cli.setex(key, int(expire), value)
