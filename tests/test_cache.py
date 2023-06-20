import asyncio
import time

from zhtools.cache import Empty, MemoryStorage, cache
from zhtools.cache.decorators import get_func_name
from zhtools.config import config


def test_get_func_name():
    def func1():
        pass

    class Foo:

        def func2(self):
            pass

        @classmethod
        def func3(cls):
            pass

        @staticmethod
        def func4():
            pass

        def __call__(self, *args, **kwargs):
            pass

    assert get_func_name(func1) == 'func1'
    assert get_func_name(Foo().func2) == 'func2'
    assert get_func_name(Foo.func2) == 'func2'
    assert get_func_name(Foo.func3) == 'func3'
    assert get_func_name(Foo.func4) == 'func4'
    assert get_func_name(Foo()) == 'Foo'


def test_cache():
    called = 0

    @cache
    def foo(i):
        nonlocal called
        called += 1
        return i * i if i < 3 else None

    assert called == 0
    assert foo(1) == 1
    assert called == 1
    assert foo(2) == 4
    assert called == 2
    assert foo(2) == 4
    assert called == 2
    assert foo(4) is None
    assert called == 3
    assert foo(4) is None
    assert called == 3


def test_method():
    called = 0

    class Foo:
        @cache
        def foo1(self, i):
            nonlocal called
            called += 1
            return i * i

    obj = Foo()
    assert obj.foo1(1) == 1
    assert called == 1
    assert obj.foo1(1) == 1
    assert called == 1
    assert obj.foo1(2) == 4
    assert called == 2

    obj2 = Foo()
    assert obj2.foo1(1) == 1
    assert called == 3
    assert obj2.foo1(1) == 1
    assert called == 3


def test_classmethod():
    called = 0

    class Foo:
        @cache
        @classmethod
        def foo1(cls, i):
            nonlocal called
            called += 1
            return i * i

    obj = Foo
    assert obj.foo1(1) == 1
    assert called == 1
    assert obj.foo1(1) == 1
    assert called == 1
    assert obj.foo1(2) == 4
    assert called == 2


class AsyncMemoryStorage(MemoryStorage):
    async def get(self, key: str):
        val, expire = self.data.get(key, (Empty, 0))
        if val is Empty:
            return val

        if expire < time.time():
            del self.data[key]
            return Empty
        return val

    async def setex(self, key: str, value, expire: float):
        if expire is None:
            expire = float('inf')
        expire_at = time.time() + expire
        self.data[key] = (value, expire_at)


def test_async():
    config.storage = AsyncMemoryStorage()

    @cache
    async def foo(i):
        return i * i

    async def run():
        await foo(1)
        await foo(1)
        await foo(2)

    asyncio.run(run())
