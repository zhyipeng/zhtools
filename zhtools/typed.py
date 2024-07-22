from collections.abc import Callable
from decimal import Decimal
from typing import Awaitable, Concatenate, ParamSpec, Protocol, TypeAlias, TypeVar


class ClassType(Protocol):
    def __init__(self, *args, **kwargs): ...


class LoggerType(Protocol):
    def debug(self, msg: str, *args, **kwargs): ...

    def info(self, msg: str, *args, **kwargs): ...

    def warning(self, msg: str, *args, **kwargs): ...

    def error(self, msg: str, *args, **kwargs): ...

    def critical(self, msg: str, *args, **kwargs): ...

    def exception(self, msg: str, *args, **kwargs): ...


P = ParamSpec("P")
R = TypeVar("R")
AwaitableR = Awaitable[R]

CommonWrapped = Callable[P, R]
CommonWrapper = Callable[P, R]

AsyncWrapped = Callable[Concatenate[P], AwaitableR]
AsyncWrapper = Callable[P, AwaitableR]

AnyCallable = Callable[P, R]
AnyAsyncCallable = Callable[P, AwaitableR]

AnyNumber: TypeAlias = int | float | complex | Decimal

NumberGeneric = TypeVar("NumberGeneric", bound=AnyNumber)
