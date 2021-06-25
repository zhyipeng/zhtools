import functools
from collections import defaultdict
from threading import current_thread
from typing import Callable, Optional, Type

__defer_stacks = defaultdict(list)
__exceptions = {}
__defer_ctx = set()


def defer_ctx(func: Callable):
    """
    Just like defer in Golang.
    >>> @defer_ctx
    >>> def foo():
    >>>     defer(lambda: print('end'))
    >>>     print(1)
    >>>     print(2)
    >>> foo()
        1
        2
        end
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        thread_id = current_thread().ident
        __defer_ctx.add(thread_id)

        ret = None
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            __exceptions[thread_id] = e

        try:
            for callback, ag, kw in reversed(__defer_stacks[thread_id]):
                callback(*ag, **kw)
        except:
            raise
        finally:
            __defer_stacks[thread_id].clear()
            __defer_ctx.remove(thread_id)

        exc = __exceptions.pop(thread_id, None)
        if exc is not None:
            raise exc

        return ret

    return wrapped


def defer(func: Callable, *args, **kwargs):
    thread_id = current_thread().ident
    assert thread_id in __defer_ctx, 'defer must called in defer context(use defer_ctx).'
    __defer_stacks[thread_id].append((func, args, kwargs))


def recover() -> Optional[Type[Exception]]:
    """
    Recover exception for defer
    >>> @defer_ctx
    >>> def foo():
    >>>     defer(lambda: print(recover()))
    >>>     print(1)
    >>>     1 / 0
    >>>     print(2)
    >>> foo()
        1
        division by zero

    """
    thread_id = current_thread().ident
    return __exceptions.pop(thread_id)
