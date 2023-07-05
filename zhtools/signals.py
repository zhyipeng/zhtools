import asyncio
from collections import defaultdict
from typing import TypeAlias, overload

from zhtools.config import config
from zhtools.typing import AnyCallable, CommonWrapper, CommonWrapped, P, R

Signal: TypeAlias = str


class Dispatcher:

    def __init__(self, multi=False):
        self.handlers: dict[Signal, list[AnyCallable]] = defaultdict(list)
        self.multi = multi

    def _register(self, signal: Signal, handler: AnyCallable):
        if self.multi:
            self.handlers[signal].append(handler)
        else:
            if signal in self.handlers:
                config.log_warning(f'Overwrite signal handler: {signal}-{handler.__name__}')

            self.handlers[signal] = [handler]

    @overload
    def register(self, signal: Signal) -> CommonWrapper:
        ...

    @overload
    def register(self, signal: Signal, handler: CommonWrapped) -> None:
        ...

    def register(self, signal: Signal, handler: CommonWrapped = None) -> CommonWrapper | None:
        if handler is not None:
            self._register(signal, handler)
            return

        def wrapper(func: CommonWrapped) -> CommonWrapper:
            self._register(signal, func)
            return func

        return wrapper

    def unregister(self, signal: Signal, handler: CommonWrapped):
        if signal not in self.handlers:
            return

        if handler not in self.handlers[signal]:
            return

        self.handlers[signal].remove(handler)

    def send(self, signal: Signal, *args: P.args, **kwargs: P.kwargs) -> R:
        result = []
        for v in self.handlers[signal]:
            ret = v(*args, **kwargs)
            result.append(ret)

        return result if self.multi else (result[0] if result else None)


class AsyncDispatcher(Dispatcher):

    async def send(self, signal: Signal, *args: P.args, **kwargs: P.kwargs) -> R:
        tasks = []
        for v in self.handlers[signal]:
            tasks.append(v(*args, **kwargs))

        if not tasks:
            return [] if self.multi else None

        ret = await asyncio.gather(*tasks)
        if self.multi:
            return ret
        return ret[0]

    def delay(self, signal: Signal, *args: P.args, **kwargs: P.kwargs):
        asyncio.create_task(self.send(signal, *args, **kwargs))
