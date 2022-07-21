import dataclasses
import datetime
import typing

if typing.TYPE_CHECKING:
    from zhtools.cache import Storage

__all__ = ['config']


@dataclasses.dataclass
class Config:
    _storage: 'Storage' = None
    default_expire: int = None
    TZ: datetime.timezone = datetime.timezone.utc

    @property
    def storage(self):
        if self._storage is None:
            from zhtools.cache import MemoryStorage
            self._storage = MemoryStorage()
        return self._storage

    @storage.setter
    def storage(self, val: 'Storage'):
        self._storage = val


config = Config()
