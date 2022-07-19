import datetime
from typing import Union, Generator

from zhtools.config import config

datetime_format = '%Y-%m-%d %H:%M:%S'
date_format = '%Y-%m-%d'
compact_datetime_format = '%Y%m%d%H%M%S'
compact_date_format = '%Y%m%d'


def set_tz(offset: Union[int, datetime.timedelta, datetime.timezone]):
    if isinstance(offset, int):
        offset = datetime.timezone(datetime.timedelta(hours=offset))
    elif isinstance(offset, datetime.timedelta):
        offset = datetime.timezone(offset)

    assert isinstance(offset, datetime.timezone)
    config.TZ = offset


def local_datetime(days: int = None, with_tz: bool = True):
    _tz = config.TZ if with_tz else None
    dt = datetime.datetime.now(tz=_tz)
    td = None
    if days:
        td = datetime.timedelta(days=days)
    if td:
        dt += td
    return dt


def timestamp_to_datetime(ts: int, with_tz: bool = True) -> datetime.datetime:
    _tz = config.TZ if with_tz else None
    return datetime.datetime.fromtimestamp(ts, tz=_tz)


def datetime_to_timestamp(dt: datetime.datetime) -> int:
    return int(dt.timestamp())


def date_to_datetime(dt: datetime.date, with_tz: bool = True) -> datetime.datetime:
    _tz = config.TZ if with_tz else None
    return datetime.datetime(year=dt.year,
                             month=dt.month,
                             day=dt.day,
                             tzinfo=_tz)


def date_from_string(date_str: str, format: str = date_format) -> datetime.date:
    return datetime.datetime.strptime(date_str, format).date()


start_of_date = date_to_datetime


def end_of_date(dt: datetime.date, with_tz: bool = True) -> datetime.datetime:
    return date_to_datetime(dt, with_tz) + datetime.timedelta(
        days=1) - datetime.timedelta(seconds=1)


def date_to_datetime_range(dt: datetime.date,
                           with_tz: bool = True,
                           ) -> tuple[datetime.datetime, datetime.datetime]:
    return start_of_date(dt, with_tz), end_of_date(dt, with_tz)


def clean_datetime(dt: datetime.datetime) -> datetime.datetime:
    """any datetime to aware datetime"""
    tz = config.TZ or datetime.timezone.utc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
        dt = tz.fromutc(dt)
    else:
        dt = dt.astimezone(tz)

    return dt


def format_datetime(dt: datetime.datetime) -> str:
    dt = clean_datetime(dt)
    return dt.strftime(datetime_format)


def iter_date(st: datetime.date,
              et: datetime.date,
              reverse=False) -> Generator[datetime.date, None, None]:
    if reverse:
        for t in reverse_iter_date(st, et):
            yield t
    else:
        t = st
        while t <= et:
            yield t
            t += datetime.timedelta(1)


def reverse_iter_date(st: datetime.date,
                      et: datetime.date
                      ) -> Generator[datetime.date, None, None]:
    t = et
    while t >= st:
        yield t
        t -= datetime.timedelta(1)
