import functools
from typing import TypeVar

from zhtools.typing import ClassType, CommonWrapped, P, R


T = TypeVar('T', bound=ClassType)


def singleton(cls_: T) -> T:
    """mark a class as singleton."""
    init = cls_.__init__

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance__'):
            cls_.__instance__ = object.__new__(cls)
            init(cls_.__instance__, *args, **kwargs)
        return cls_.__instance__

    cls_.__new__ = __new__
    cls_.__init__ = lambda *args, **kwargs: None
    return cls_


def property_with_cache(meth: CommonWrapped) -> R:
    """
    Add an underscore before the property name for caching.
    >>> class Foo
    >>>     @property_with_cache
    >>>     def prop1(self) -> str:
    >>>         return 'prop1'

    >>> foo = Foo()
    >>> foo.prop1
    True
    >>> getattr(foo, '_prop1')
    True
    """
    @functools.wraps(meth)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        instance = args[0]
        property_name = meth.__name__
        private_prop_name = '_' + property_name
        if not getattr(instance, private_prop_name, False):
            setattr(instance, private_prop_name, meth(*args, **kwargs))
        return getattr(instance, private_prop_name, None)

    return property(wrapper)
