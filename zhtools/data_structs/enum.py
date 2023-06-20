import typing
from enum import Enum as BaseEnum
from typing import Generic, TypeVar


class _Enum(BaseEnum):
    def __new__(cls, value: typing.Any, label: str = None):
        if label is not None:
            assert isinstance(label, str)
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label = label
        return obj

    @property
    def label(self) -> str:
        return self._label or self.name

    @classmethod
    def labels(cls) -> dict[typing.Any, str]:
        return {e.value: e.label for e in cls}

    @classmethod
    def options(cls) -> tuple[tuple[typing.Any, str]]:
        return tuple((e.value, e.label) for e in cls)


if typing.TYPE_CHECKING:
    T = TypeVar('T')

    class Enum(Generic[T], BaseEnum):
        @property
        def value(self) -> T: ...
        @property
        def label(self) -> str: ...
        @classmethod
        def labels(cls) -> dict[T, str]: ...
        @classmethod
        def options(cls) -> tuple[tuple[T, str]]: ...

    class IntEnum(Enum['int']):
        @property
        def value(self) -> int: ...
        @property
        def label(self) -> str: ...
        @classmethod
        def labels(cls) -> dict[int, str]: ...
        @classmethod
        def options(cls) -> tuple[tuple[int, str]]: ...

    class StrEnum(Enum['int']):
        @property
        def value(self) -> str: ...
        @property
        def label(self) -> str: ...
        @classmethod
        def labels(cls) -> dict[str, str]: ...
        @classmethod
        def options(cls) -> tuple[tuple[str, str]]: ...

else:
    Enum = _Enum
    IntEnum = _Enum
    StrEnum = _Enum
