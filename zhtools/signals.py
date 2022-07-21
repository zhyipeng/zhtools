import asyncio
import typing

from zhtools import AnyCallable

Signal = typing.NewType('Signal', str)


class Dispatcher:

    def __init__(self, multi: bool = False):
        self.handlers: dict[Signal, list[AnyCallable]] = {}
        self.multi = multi

    def _register(self, signal: Signal, handler: AnyCallable):
        if signal not in self.handlers:
            self.handlers[signal] = [handler]
        else:
            if self.multi:
                self.handlers[signal].append(handler)
            else:
                self.handlers[signal] = [handler]

    def register(self, signal: Signal, handler: AnyCallable = None):
        if handler is not None:
            self._register(signal, handler)
            return

        def wrapper(func: AnyCallable):
            self._register(signal, func)
            return func

        return wrapper

    def send(self, signal: Signal, *args, **kwargs) -> typing.Any:
        result = []
        for v in self.handlers.get(signal, []):
            ret = v(*args, **kwargs)
            result.append(ret)

        return result if self.multi else (result[0] if result else None)


class AsyncDispatcher(Dispatcher):

    async def send(self, signal: Signal, *args, **kwargs) -> typing.Any:
        tasks = []
        for v in self.handlers.get(signal, []):
            tasks.append(v(*args, **kwargs))

        ret = await asyncio.gather(*tasks)
        return ret if self.multi else (ret[0] if ret else None)
