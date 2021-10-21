import abc
from pathlib import Path
from typing import Any, Generator


class ReaderInterface(metaclass=abc.ABCMeta):

    def __init__(self, path: Path):
        self.path = path

    @abc.abstractmethod
    def read(self) -> Any:
        pass

    @abc.abstractmethod
    def readlines(self) -> list[Any]:
        pass

    @abc.abstractmethod
    def readline(self) -> Generator[Any, None, None]:
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_val:
            raise exc_val
