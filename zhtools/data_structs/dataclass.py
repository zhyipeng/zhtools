from dataclasses import dataclass, is_dataclass


def nested_dataclass(*args, **kwargs):
    """
    >>> @dataclass
    >>> class A:
    >>>     m: int
    >>> @dataclass
    >>> class B:
    >>>     a: A
    >>> B(a={'m', 1})
    B(a={'m': 1})
    # The type of B.a is actually dict
    >>> @nested_dataclass
    >>> class C:
    >>>     a: A
    >>> C(a={'m': 1})
    C(a=A(m=1))
    # The type of B.a is actually A
    """

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)  # type: ignore

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper
