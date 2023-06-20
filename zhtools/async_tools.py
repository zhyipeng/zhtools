import asyncio
import functools

from zhtools.typing import AsyncWrapped, CommonWrapper, P, R


def as_sync_func(loop: asyncio.AbstractEventLoop = None):
    """decorate an async function to sync function"""

    def decorator(func: AsyncWrapped) -> CommonWrapper:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal loop
            if not loop:
                if args and isinstance(args[0], asyncio.AbstractEventLoop):
                    return args[0].run_until_complete(func(*args[1:], **kwargs))
                else:
                    loop = asyncio.get_event_loop()
            return loop.run_until_complete(func(*args, **kwargs))

        return wrapper

    return decorator
