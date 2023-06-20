import dataclasses
import datetime
import typing

from zhtools.typing import LoggerType

if typing.TYPE_CHECKING:
    from zhtools.cache.storages import Storage

__all__ = ['config']


def _get_sys_tz():
    return datetime.datetime.now().astimezone().tzinfo


@dataclasses.dataclass
class Config:
    TZ: datetime.timezone = _get_sys_tz()
    logger: LoggerType | None = None

    # cache
    _storage: 'Storage' = None
    default_expire: int = None

    def set_tz(self, tz: datetime.timezone):
        self.TZ = tz

    def set_logger(self, logger: LoggerType):
        self.logger = logger

    @property
    def storage(self):
        if self._storage is None:
            from zhtools.cache.storages import MemoryStorage
            self._storage = MemoryStorage()
        return self._storage

    @storage.setter
    def storage(self, val: 'Storage'):
        self._storage = val

    def log_debug(self, msg: str, *args, **kwargs):
        if self.logger:
            self.logger.debug(msg, *args, **kwargs)

    def log_info(self, msg: str, *args, **kwargs):
        if self.logger:
            self.logger.info(msg, *args, **kwargs)

    def log_warning(self, msg: str, *args, **kwargs):
        if self.logger:
            self.logger.warning(msg, *args, **kwargs)

    def log_error(self, msg: str, *args, **kwargs):
        if self.logger:
            self.logger.error(msg, *args, **kwargs)

    def log_exception(self, msg: str, *args, **kwargs):
        if self.logger:
            self.logger.exception(msg, *args, **kwargs)


config = Config()
