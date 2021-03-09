import functools
from contextlib import contextmanager
from inspect import isfunction
from typing import Callable, Optional, Union

from zhtools import ignore_exception
from zhtools.exceptions import ModuleRequired

_redis_pool = None
_redis_client = None


def init(redis_client=None, redis_pool=None):
    global _redis_pool
    global _redis_client
    _redis_client = redis_client
    _redis_pool = redis_pool


def get_client():
    if _redis_client:
        return _redis_client
    if _redis_pool:
        try:
            import redis
            return redis.Redis(connection_pool=_redis_client)
        except ImportError:
            raise ModuleRequired('redis')


@contextmanager
def concurrent_lock(key: str,
                    ttl: int = 3,
                    blocking_timeout: Optional[int] = None,
                    redis_cli=None):
    """
    >>> with concurrent_lock(key='lock') as l:
    >>>     if not l:
    >>>         raise Exception()
    >>>     ...
    """
    redis_cli = redis_cli or get_client()
    lock = redis_cli.lock(key,
                          timeout=ttl,
                          blocking_timeout=blocking_timeout)
    locked = lock.acquire()

    try:
        yield locked
    finally:
        if locked:
            with ignore_exception():
                lock.release()


class GetLockError(Exception):
    pass


def concurrent_limit(key: Union[str, Callable],
                     ttl: int = 3,
                     blocking_timeout: Optional[int] = None):
    """
    Use directly
    >>> @concurrent_limit
    >>> def foo(k):
    >>>     pass

    Use with parameters
    >>> @concurrent_limit(key='lock')
    >>> def foo():
    >>>     pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            nonlocal key
            if isfunction(key):
                key = key.__name__

            with concurrent_lock(key, ttl, blocking_timeout) as lock:
                if not lock:
                    raise GetLockError()
                return func(*args, **kwargs)

        return wrapped

    if isfunction(key):
        return decorator(key)

    return decorator
