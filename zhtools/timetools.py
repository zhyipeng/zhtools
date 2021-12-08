import datetime
from typing import Optional, Union

datetime_format = '%Y-%m-%d %H:%M:%S'
date_format = '%Y-%m-%d'
compact_datetime_format = '%Y%m%d%H%M%S'
compact_date_format = '%Y%m%d'

TZ: Optional[datetime.timezone] = datetime.timezone.utc


def set_tz(offset: Union[int, datetime.timedelta, datetime.timezone]):
    if isinstance(offset, int):
        offset = datetime.timezone(datetime.timedelta(hours=offset))
    elif isinstance(offset, datetime.timedelta):
        offset = datetime.timezone(offset)

    assert isinstance(offset, datetime.timezone)
    global TZ
    TZ = offset


def local_datetime(days: int = None, with_tz: bool = True):
    _tz = TZ if with_tz else None
    dt = datetime.datetime.now(tz=_tz)
    td = None
    if days:
        td = datetime.timedelta(days=days)
    if td:
        dt += td
    return dt


def timestamp_to_datetime(ts: int, with_tz: bool = True) -> datetime.datetime:
    _tz = TZ if with_tz else None
    return datetime.datetime.fromtimestamp(ts, tz=_tz)


def datetime_to_timestamp(dt: datetime.datetime) -> int:
    return int(dt.timestamp())


def date_to_datetime(dt: datetime.date, with_tz: bool = True) -> datetime.datetime:
    _tz = TZ if with_tz else None
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
