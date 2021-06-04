import asyncio
from threading import Thread
from multiprocessing import Process
from typing import Any, Callable, Coroutine, Type, Union

TASK_TYPE = Union[Thread, Process]
TASK_CLI_TYPE = Type[TASK_TYPE]


class ConcurrentMixin:
    _task_cli: TASK_CLI_TYPE = None

    def __init__(self):
        self._tasks: list[TASK_TYPE] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._run()
        else:
            if exc_val is None:
                exc_val = exc_type()
            raise exc_val

    def execute(self, func: Callable[..., Any], *args, **kwargs):
        self._tasks.append(self._task_cli(target=func, args=args, kwargs=kwargs))

    def _run(self):
        for t in self._tasks:
            t.start()
        for t in self._tasks:
            t.join()


class ThreadConcurrent(ConcurrentMixin):
    _task_cli = Thread


class ProcessConcurrent(ConcurrentMixin):
    _task_cli = Process


class CoroutineConcurrent:

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

    def execute(self, func: Callable[..., Any], *args, **kwargs):
        self._tasks.append(func(*args, **kwargs))

    async def _run(self):
        await asyncio.gather(*self._tasks)
        self._tasks.clear()

    async def execute_batch(self, tasks: list[Coroutine]):
        self._tasks.extend(tasks)
        await self._run()
