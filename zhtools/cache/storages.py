import abc
import logging
import pickle
import time
import typing

if typing.TYPE_CHECKING:
    from redis import Redis


Empty = object()


class Storage[T](metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key: str) -> T:
        pass

    def set(self, key: str, value: T):
        self.setex(key, value, float("inf"))

    @abc.abstractmethod
    def setex(self, key: str, value: T, expire: float):
        pass


class AsyncStorage[T](Storage, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, key: str) -> T:
        pass

    async def set(self, key: str, value: T):
        await self.setex(key, value, float("inf"))

    @abc.abstractmethod
    async def setex(self, key: str, value: T, expire: float):
        pass


class MemoryStorage[T](Storage):
    def __init__(self):
        self.data: dict[str, tuple[T, float]] = {}

    def get(self, key: str) -> T | object:
        val, expire = self.data.get(key, (Empty, 0))
        if val is Empty:
            return val

        if expire < time.time():
            del self.data[key]
            return Empty
        return val

    def setex(self, key: str, value: T, expire: float):
        if expire is None:
            expire = float("inf")
        expire_at = time.time() + expire
        self.data[key] = (value, expire_at)


class RedisStorage[T](Storage):
    def __init__(self, redis_cli: "Redis"):
        self.redis_cli = redis_cli

    def get(self, key: str) -> T | object:
        ret = self.redis_cli.get(key)
        if ret is None:
            return Empty

        if isinstance(ret, bytes):
            try:
                ret = pickle.loads(ret)
            except pickle.UnpicklingError:
                pass

        return ret

    def setex(self, key: str, value: T, expire: float):
        try:
            _value = pickle.dumps(value)
        except pickle.PickleError:
            logging.error(f"cache value {value} can not pickle.")
            return

        if expire is None or expire == float("inf"):
            self.redis_cli.set(key, _value)
        else:
            self.redis_cli.setex(key, int(expire), _value)


class AsyncRedisStorage[T](AsyncStorage):
    def __init__(self, redis_cli: "Redis"):
        self.redis_cli = redis_cli

    async def get(self, key: str) -> T | object:
        ret = await self.redis_cli.get(key)
        if ret is None:
            return Empty

        if isinstance(ret, bytes):
            try:
                ret = pickle.loads(ret)
            except pickle.UnpicklingError:
                pass

        return ret

    async def setex(self, key: str, value: T, expire: float):
        try:
            _value = pickle.dumps(value)
        except pickle.PickleError:
            logging.error(f"cache value {value} can not pickle.")
            return

        if expire is None or expire == float("inf"):
            await self.redis_cli.set(key, _value)
        else:
            await self.redis_cli.setex(key, int(expire), _value)
