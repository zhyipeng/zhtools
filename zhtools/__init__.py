import functools
import inspect
import logging
from collections import defaultdict
from contextlib import contextmanager
from typing import Any, Callable

from zhtools.type_hint import AnyCallable, AnyNumber


def property_with_cache(func: Callable):
    """
    Add an underscore before the property name for caching.
    >>> class Foo
    >>>     @property_with_cache
    >>>     def prop1(self):
    >>>         return True

    >>> foo = Foo()
    >>> foo.prop1
    True
    >>> getattr(foo, '_prop1')
    True
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        instance = args[0]
        property_name = func.__name__
        private_prop_name = '_' + property_name
        if not getattr(instance, private_prop_name, False):
            setattr(instance, private_prop_name, func(*args, **kwargs))
        return getattr(instance, private_prop_name, None)

    return property(wrapped)


@contextmanager
def ignore_exception(logger: logging.Logger = None):
    try:
        yield
    except:
        if logger:
            logger.exception('Exception raise but has been ignored.')


def safe_divide(a: AnyNumber,
                b: AnyNumber,
                decimal_len: int = 2,
                while_zero: AnyNumber = 0) -> str:
    """
    Safe division avoiding ZeroDivisionError
    :param a: dividend
    :param b: divisor
    :param decimal_len: decimal digits
    :param while_zero:
    :return: division result
    """
    fm = f'%.{decimal_len}f'
    return fm % (a / b) if b else fm % while_zero


def singleton(cls_):
    """
    singleton decorator for class.
    """
    init = cls_.__init__

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance__'):
            cls_.__instance__ = object.__new__(cls)
            init(cls_.__instance__, *args, **kwargs)
        return cls_.__instance__

    cls_.__new__ = __new__
    cls_.__init__ = lambda *args, **kwargs: None
    return cls_


def group_by_key(data: list, key: str) -> dict[str, list]:
    ret = defaultdict(list)
    for item in data:
        k = getattr(item, key)
        ret[k].append(item)

    return dict(ret)


def package_func_kwargs(func: AnyCallable,
                        *args,
                        **kwargs) -> dict[str, Any]:
    """convert calling args to kwargs"""
    if not args:
        return kwargs

    kw = {}
    params = list(inspect.signature(func).parameters.keys())
    for i, v in enumerate(args):
        kw[params[i]] = v

    return kw | kwargs
