from decimal import Decimal
from typing import Any, AnyStr, Callable, TypeVar

AnyNumber = TypeVar('AnyNumber', int, float, Decimal)

AnyCallable = Callable[[...], Any]

Wrapped = Callable[[...], Any]

Decorator = Callable[[Wrapped], Wrapped]

MakeCacheKeyFunc = Callable[[Wrapped, ...], AnyStr]
