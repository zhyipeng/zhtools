import asyncio
import typing
from collections.abc import Coroutine
from multiprocessing import Lock as MpLock
from multiprocessing import Process
from threading import Lock as ThLock
from threading import Thread
from typing import Generic, Type, TypeVar, Union

from zhtools.typing import AnyCallable, CommonWrapped, CommonWrapper, P, R

if typing.TYPE_CHECKING:
    from multiprocessing.synchronize import Lock as TMpLock

TASK_TYPE = Union[Thread, Process]
TASK_CLI_TYPE = Type[TASK_TYPE]

T = TypeVar("T", bound=TASK_TYPE)


class ConcurrentMixin(Generic[T]):
    _task_cli: type[T]

    def __init__(self):
        self._tasks: list[T] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._run()
        else:
            if exc_val is None:
                exc_val = exc_type()
            raise exc_val

    def execute(self, func: AnyCallable, *args, **kwargs):
        self._tasks.append(self._task_cli(target=func, args=args, kwargs=kwargs))

    def _run(self):
        for t in self._tasks:
            t.start()
        for t in self._tasks:
            t.join()


class ThreadConcurrent(ConcurrentMixin):
    """
    concurrency with thread
    >>> with ThreadConcurrent() as c:
    >>>     c.execute(print, 1)
    """

    _task_cli = Thread


class ProcessConcurrent(ConcurrentMixin):
    """
    concurrency with subprocess
    >>> with ThreadConcurrent() as c:
    >>>     c.execute(print, 1)
    """

    _task_cli = Process


class CoroutineConcurrent:
    """
    concurrency with coroutine
    >>> async with CoroutineConcurrent() as c:
    >>>     c.execute(asyncio.sleep(1))
    """

    def __init__(self):
        self._tasks: list[Coroutine] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            asyncio.run(self._run())
        else:
            if exc_val is None:
                exc_val = exc_type()
            raise exc_val

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self._run()
        else:
            if exc_val is None:
                exc_val = exc_type()
            raise exc_val

    def execute(self, cor: Coroutine):
        self._tasks.append(cor)

    async def _run(self):
        await asyncio.gather(*self._tasks)
        self._tasks.clear()

    async def execute_batch(self, tasks: list[Coroutine]):
        self._tasks.extend(tasks)
        await self._run()


__thread_lock_map: dict[str, ThLock] = {}


def with_memory_thread_lock(f: CommonWrapped) -> CommonWrapper:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        k = f.__qualname__
        if k not in __thread_lock_map:
            __thread_lock_map[k] = ThLock()
        lock = __thread_lock_map[k]
        with lock:
            return f(*args, **kwargs)

    return inner


__process_lock_map: dict[str, "TMpLock"] = {}


def with_memory_process_lock(f: CommonWrapped) -> CommonWrapper:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        k = f.__qualname__
        if k not in __process_lock_map:
            __process_lock_map[k] = MpLock()
        lock = __process_lock_map[k]
        with lock:
            return f(*args, **kwargs)

    return inner


__coroutine_lock_map: dict[str, asyncio.Lock] = {}


def with_memory_coroutine_lock(f: CommonWrapped) -> CommonWrapper:
    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        k = f.__qualname__
        if k not in __coroutine_lock_map:
            __coroutine_lock_map[k] = asyncio.Lock()
        lock = __coroutine_lock_map[k]
        async with lock:
            return await f(*args, **kwargs)

    return inner
