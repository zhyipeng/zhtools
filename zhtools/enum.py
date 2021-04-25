from enum import Enum as BaseEnum
from typing import Any


class Enum(BaseEnum):

    def __new__(cls, value, label: str = None):
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
    def labels(cls) -> dict[Any, str]:
        return {e.value: e.label for e in cls}

    @classmethod
    def options(cls) -> tuple[tuple[Any, str]]:
        return tuple((e.value, e.label) for e in cls)
