import datetime
from collections.abc import Generator
from enum import StrEnum


class Format(StrEnum):
    datetime = "%Y-%m-%d %H:%M:%S"
    date = "%Y-%m-%d"
    compact_datetime = "%Y%m%d%H%M%S"
    compact_date = "%Y%m%d"


def date_to_datetime(dt: datetime.date) -> datetime.datetime:
    return datetime.datetime(year=dt.year, month=dt.month, day=dt.day)


start_of_date = date_to_datetime


def end_of_date(dt: datetime.date) -> datetime.datetime:
    return (
        date_to_datetime(dt)
        + datetime.timedelta(days=1)
        - datetime.timedelta(milliseconds=1)
    )


def date_to_datetime_range(
    dt: datetime.date, with_tz: bool = True
) -> tuple[datetime.datetime, datetime.datetime]:
    return start_of_date(dt), end_of_date(dt)


def string_to_date(date_str: str, format: str = Format.date) -> datetime.date:
    return datetime.datetime.strptime(date_str, format).date()


def iter_date(
    st: datetime.date,
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


def reverse_iter_date(
    st: datetime.date,
    et: datetime.date,
) -> Generator[datetime.date, None, None]:
    t = et
    while t >= st:
        yield t
        t -= datetime.timedelta(days=1)


class ZHDatetime:
    def __init__(
        self,
        dt: datetime.datetime | datetime.date | int | str | None = None,
    ):
        if dt is None:
            dt = datetime.datetime.now()
        elif isinstance(dt, int):
            dt = datetime.datetime.fromtimestamp(dt)
        elif isinstance(dt, str):
            length = len(dt)
            match length:
                case 8:
                    dt = string_to_date(dt, Format.compact_date)
                    dt = date_to_datetime(
                        dt,
                    )
                case 10:
                    dt = string_to_date(dt)
                    dt = date_to_datetime(dt)
                case 14:
                    dt = datetime.datetime.strptime(dt, Format.compact_datetime)
                case 19:
                    dt = datetime.datetime.strptime(dt, Format.datetime)
                case _:
                    raise ValueError(f"Invalid datetime string: {dt}")
        elif isinstance(dt, datetime.datetime):
            pass
        elif isinstance(dt, datetime.date):
            dt = date_to_datetime(dt)

        self.dt = dt

    def __repr__(self):
        return repr(self.dt)

    def __str__(self):
        return str(self.dt)

    def format(self, fmt: str = Format.datetime) -> str:
        return self.dt.strftime(fmt)

    @property
    def timestamp(self) -> int:
        return int(self.dt.timestamp())

    @property
    def date(self) -> datetime.date:
        return self.dt.date()

    @property
    def time(self) -> datetime.time:
        return self.dt.time()

    @property
    def date_range(self) -> tuple[datetime.datetime, datetime.datetime]:
        return date_to_datetime_range(self.date)

    @property
    def start_of_date(self) -> datetime.datetime:
        return start_of_date(self.date)

    @property
    def end_of_date(self) -> datetime.datetime:
        return end_of_date(self.date)
