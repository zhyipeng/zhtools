import asyncio
from collections import defaultdict
from typing import Callable, TypeAlias, overload

from zhtools.config import config

Signal: TypeAlias = str


class Dispatcher[T, **P]:
    def __init__(self, multi=False):
        self.handlers: dict[Signal, list[Callable[P, T]]] = defaultdict(list)
        self.multi = multi

    def _register(self, signal: Signal, handler: Callable[P, T]):
        if self.multi:
            self.handlers[signal].append(handler)
        else:
            if signal in self.handlers:
                config.log_warning(
                    f"Overwrite signal handler: {signal}-{handler.__name__}"
                )

            self.handlers[signal] = [handler]

    @overload
    def register(
        self, signal: Signal
    ) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

    @overload
    def register(self, signal: Signal, handler: Callable[P, T]) -> None: ...

    def register(
        self, signal: Signal, handler: Callable[P, T] | None = None
    ) -> Callable[[Callable[P, T]], Callable[P, T]] | None:
        if handler is not None:
            self._register(signal, handler)
            return

        def wrapper(func: Callable[P, T]) -> Callable[P, T]:
            self._register(signal, func)
            return func

        return wrapper

    def unregister(self, signal: Signal, handler: Callable[P, T]):
        if signal not in self.handlers:
            return

        if handler not in self.handlers[signal]:
            return

        self.handlers[signal].remove(handler)

    def send(
        self, signal: Signal, *args: P.args, **kwargs: P.kwargs
    ) -> T | list[T] | None:
        result = []
        for v in self.handlers[signal]:
            ret = v(*args, **kwargs)
            result.append(ret)

        return result if self.multi else (result[0] if result else None)


class AsyncDispatcher[T, **P](Dispatcher):
    async def send(
        self, signal: Signal, *args: P.args, **kwargs: P.kwargs
    ) -> T | list[T] | None:
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
