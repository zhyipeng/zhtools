import asyncio
import logging
from asyncio.tasks import Task
from typing import Any, Callable, Coroutine


class Promise:
    """
    run coroutine like js promise
    >>> async def foo
    >>>     ...
    >>> Promise(foo()).then(lambda r: print(r)).catch(lambda e: print(e))()
    """

    def __init__(self, coroutine: Coroutine):
        self._coroutine = coroutine
        self._callback = None
        self._error_handler = None

    def default_callback(self, task: Task):
        exc = task.exception()
        if exc:
            logging.info(f'promise done and raise error: {exc}')
            if self._error_handler:
                self._error_handler(exc)
        else:
            logging.info(f'promise done. result: {task.result()}')
            self._callback(task.result())

    def then(self, callback: Callable[[Any], None]):
        self._callback = callback
        return self

    def catch(self, callback: Callable[[Exception], None]):
        self._error_handler = callback
        return self

    def __call__(self, *args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            tsk = loop.create_task(self._coroutine)
            tsk.add_done_callback(self.default_callback)
        else:
            asyncio.run(self._coroutine)
