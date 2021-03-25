import datetime


datetime_format = '%Y-%m-%d %H:%M:%S'
date_format = '%Y-%m-%d'
compact_datetime_format = '%Y%m%d%H%M%S'
compact_date_format = '%Y%m%d'


def local_datetime(days: int = None):
    dt = datetime.datetime.now()
    td = None
    if days:
        td = datetime.timedelta(days=days)
    if td:
        dt += td
    return dt


def timestamp_to_datetime(ts: int,
                          tz: datetime.tzinfo = None) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ts, tz=tz)


def datetime_to_timestamp(dt: datetime.datetime) -> int:
    return int(dt.timestamp())


def date_to_datetime(dt: datetime.date) -> datetime.datetime:
    return datetime.datetime(year=dt.year,
                             month=dt.month,
                             day=dt.day)


def date_from_string(date_str: str, format: str = date_format) -> datetime.date:
    return datetime.datetime.strptime(date_str, format).date()


start_of_date = date_to_datetime


def end_of_date(dt: datetime.date) -> datetime.datetime:
    return date_to_datetime(dt) + datetime.timedelta(
        days=1) - datetime.timedelta(seconds=1)
