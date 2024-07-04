import asyncio
import functools
from typing import Awaitable, Callable


def as_sync_func(loop: asyncio.AbstractEventLoop | None = None):
    """decorate an async function to sync function"""

    def decorator[T, **P](func: Callable[P, Awaitable[T]]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            nonlocal loop
            if not loop:
                if args and isinstance(args[0], asyncio.AbstractEventLoop):
                    return args[0].run_until_complete(func(*args[1:], **kwargs))  # type: ignore
                else:
                    loop = asyncio.get_event_loop()
            return loop.run_until_complete(func(*args, **kwargs))

        return wrapper

    return decorator
