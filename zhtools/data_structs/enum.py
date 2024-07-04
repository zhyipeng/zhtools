import typing
from enum import Enum as BaseEnum


class Enum[T](BaseEnum):
    def __new__(cls, value: T, label: typing.Optional[str] = None):
        if label is not None:
            assert isinstance(label, str)
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label = label  # type: ignore
        return obj

    @property
    def label(self) -> str:
        return self._label or self.name  # type: ignore

    @classmethod
    def labels(cls) -> dict[T, str]:
        return {e.value: e.label for e in cls}

    @classmethod
    def options(cls) -> tuple[tuple[T, str]]:
        return tuple((e.value, e.label) for e in cls)  # type: ignore


if typing.TYPE_CHECKING:

    class IntEnum(Enum):
        @property
        def value(self) -> int: ...
        @property
        def label(self) -> str: ...
        @classmethod
        def labels(cls) -> dict[int, str]: ...
        @classmethod
        def options(cls) -> tuple[tuple[int, str]]: ...

    class StrEnum(Enum):
        @property
        def value(self) -> str: ...
        @property
        def label(self) -> str: ...
        @classmethod
        def labels(cls) -> dict[str, str]: ...
        @classmethod
        def options(cls) -> tuple[tuple[str, str]]: ...

else:
    IntEnum = Enum
    StrEnum = Enum
