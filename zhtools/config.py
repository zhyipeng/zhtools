import dataclasses
import datetime

from zhtools.cache.storages import MemoryStorage, Storage

__all__ = ['config']


@dataclasses.dataclass
class Config:
    storage: Storage = MemoryStorage()
    default_expire: int = None
    TZ: datetime.timezone = datetime.timezone.utc


config = Config()
