import datetime
from collections.abc import Generator
from enum import StrEnum

from zhtools.config import config


class Format(StrEnum):
    datetime = '%Y-%m-%d %H:%M:%S'
    date = '%Y-%m-%d'
    compact_datetime = '%Y%m%d%H%M%S'
    compact_date = '%Y%m%d'


def set_tz(offset: int | datetime.timedelta | datetime.timezone):
    if isinstance(offset, int):
        offset = datetime.timezone(datetime.timedelta(hours=offset))
    elif isinstance(offset, datetime.timedelta):
        offset = datetime.timezone(offset)

    assert isinstance(offset, datetime.timezone)
    config.set_tz(offset)


def local_datetime():
    """Return current datetime with local timezone."""
    return datetime.datetime.now(tz=config.TZ)


def timestamp_to_datetime(ts: int, with_tz: bool = True) -> datetime.datetime:
    tz = config.TZ if with_tz else None
    return datetime.datetime.fromtimestamp(ts, tz=tz)


def datetime_to_timestamp(dt: datetime.datetime) -> int:
    return int(dt.timestamp())


def date_to_datetime(dt: datetime.date, with_tz: bool = True) -> datetime.datetime:
    tz = config.TZ if with_tz else None
    return datetime.datetime(year=dt.year,
                             month=dt.month,
                             day=dt.day,
                             tzinfo=tz)


start_of_date = date_to_datetime


def end_of_date(dt: datetime.date, with_tz: bool = True) -> datetime.datetime:
    return date_to_datetime(dt, with_tz) + datetime.timedelta(
        days=1) - datetime.timedelta(milliseconds=1)


def date_to_datetime_range(dt: datetime.date, with_tz: bool = True
                           ) -> tuple[datetime.datetime, datetime.datetime]:
    return start_of_date(dt, with_tz), end_of_date(dt, with_tz)


def string_to_date(date_str: str, format: str = Format.date) -> datetime.date:
    return datetime.datetime.strptime(date_str, format).date()


def to_aware_datetime(dt: datetime.datetime) -> datetime.datetime:
    """
    Convert any datetime to aware datetime(local).
    If datetime is naive, it will be converted(replace) to local datetime.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=config.TZ)
        dt = config.TZ.fromutc(dt)
    else:
        dt = dt.astimezone(config.TZ)
    return dt


def iter_date(st: datetime.date,
              et: datetime.date,
              reverse: bool = False,
              ) -> Generator[datetime.date, None, None]:
    if reverse:
        yield from reverse_iter_date(st, et)
    else:
        t = st
        while t <= et:
            yield t
            t += datetime.timedelta(days=1)


def reverse_iter_date(st: datetime.date,
                      et: datetime.date,
                      ) -> Generator[datetime.date, None, None]:
    t = et
    while t >= st:
        yield t
        t -= datetime.timedelta(days=1)


class ZHDatetime:

    def __init__(self,
                 dt: datetime.datetime | datetime.date | int | str | None = None,
                 with_tz: bool = True):
        if dt is None:
            dt = local_datetime()
        elif isinstance(dt, int):
            dt = timestamp_to_datetime(dt, with_tz)
        elif isinstance(dt, str):
            length = len(dt)
            match length:
                case 8:
                    dt = string_to_date(dt, Format.compact_date)
                    dt = date_to_datetime(dt, with_tz)
                case 10:
                    dt = string_to_date(dt)
                    dt = date_to_datetime(dt, with_tz)
                case 14:
                    dt = datetime.datetime.strptime(dt, Format.compact_datetime)
                case 19:
                    dt = datetime.datetime.strptime(dt, Format.datetime)
                case _:
                    raise ValueError(f'Invalid datetime string: {dt}')
        elif isinstance(dt, datetime.datetime):
            pass
        elif isinstance(dt, datetime.date):
            dt = date_to_datetime(dt, with_tz)

        self.with_tz = with_tz
        self.dt = dt
        if with_tz:
            self.dt = to_aware_datetime(self.dt)

    def __repr__(self):
        return repr(self.dt)

    def __str__(self):
        return str(self.dt)

    def format(self, fmt: str = Format.datetime) -> str:
        return self.dt.strftime(fmt)

    @property
    def timestamp(self) -> int:
        return datetime_to_timestamp(self.dt)

    @property
    def date(self) -> datetime.date:
        return self.dt.date()

    @property
    def time(self) -> datetime.time:
        return self.dt.time()

    @property
    def date_range(self) -> tuple[datetime.datetime, datetime.datetime]:
        return date_to_datetime_range(self.date, self.with_tz)

    @property
    def start_of_date(self) -> datetime.datetime:
        return start_of_date(self.date, self.with_tz)

    @property
    def end_of_date(self) -> datetime.datetime:
        return end_of_date(self.date, self.with_tz)
