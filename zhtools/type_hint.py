from decimal import Decimal
from typing import Any, Callable, TypeVar

AnyNumber = TypeVar('AnyNumber', int, float, Decimal)
AnyCallable = Callable[[...], Any]
