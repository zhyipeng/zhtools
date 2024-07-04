import datetime

from zhtools.data_structs.convertors import camel_case_to_underline
from zhtools.timetools import Format
from zhtools.typing import ClassType


def singleton[T: ClassType](cls_: T) -> T:
    """mark a class as singleton."""
    init = cls_.__init__

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance__"):
            cls_.__instance__ = object.__new__(cls)  # type: ignore
            init(cls_.__instance__, *args, **kwargs)  # type: ignore
        return cls_.__instance__  # type: ignore

    cls_.__new__ = __new__
    cls_.__init__ = lambda *args, **kwargs: None
    return cls_


def multi_by_date[T: ClassType](cls: T) -> T:
    """
    make a SQLAlchemy model class support multi-tables by date.
    use `get_model` to get a model by date.
    example:
    >>> @multi_by_date
    >>> class MyModel(Base):
    >>>     ...
    >>> m: type[MyModel] = MyModel.get_model(datetime.date.today())
    """
    cls.__abstract__ = True  # type: ignore
    cls.__model_map__ = {}  # type: ignore
    if not hasattr(cls, "__tablename__"):
        cls.__tablename__ = camel_case_to_underline(cls.__name__)  # type: ignore

    def get_model_by_date(cls, date: datetime.date) -> T:
        tablename = f"{cls.__tablename__}{date.strftime(Format.compact_date)}"
        if tablename in cls.__model_map__:
            return cls.__model_map__[tablename]

        class _Model(cls):
            __tablename__ = tablename
            __date__ = date

        cls.__model_map__[tablename] = _Model
        return _Model

    cls.get_model = classmethod(get_model_by_date)  # type: ignore
    return cls
