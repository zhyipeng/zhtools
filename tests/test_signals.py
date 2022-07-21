import asyncio

import pytest

from zhtools.signals import AsyncDispatcher, Dispatcher


def test_signal_dispatcher():
    called = None
    dispatcher = Dispatcher()

    @dispatcher.register('foo1')
    def foo1():
        nonlocal called
        called = 'foo1'
        return 1


    @dispatcher.register('foo2')
    def foo2():
        nonlocal called
        called = 'foo2'
        return 2

    assert called is None
    ret = dispatcher.send('foo1')
    assert ret == 1
    assert called == 'foo1'

    ret = dispatcher.send('foo2')
    assert ret == 2
    assert called == 'foo2'

    ret = dispatcher.send('foo3')
    assert called == 'foo2'
    assert ret is None


def test_multi_signal_dispatcher():
    called = None
    dispatcher = Dispatcher(multi=True)

    @dispatcher.register('foo1')
    def foo1():
        nonlocal called
        called = 'foo1'
        return 1


    @dispatcher.register('foo1')
    def foo2():
        nonlocal called
        called = 'foo2'
        return 2

    assert called is None
    ret = dispatcher.send('foo1')
    assert ret == [1, 2]
    assert called == 'foo2'

    ret = dispatcher.send('foo3')
    assert called == 'foo2'
    assert ret == []


@pytest.mark.asyncio
async def test_async_signal_dispatcher():
    called = None
    dispatcher = AsyncDispatcher()

    @dispatcher.register('foo1')
    async def foo1():
        nonlocal called
        called = 'foo1'
        return 1

    @dispatcher.register('foo2')
    async def foo2():
        nonlocal called
        called = 'foo2'
        return 2

    assert called is None
    ret = await dispatcher.send('foo1')
    assert ret == 1
    assert called == 'foo1'

    ret = await dispatcher.send('foo2')
    assert ret == 2
    assert called == 'foo2'

    ret = await dispatcher.send('foo3')
    assert called == 'foo2'
    assert ret is None


@pytest.mark.asyncio
async def test_async_multi_signal_dispatcher():
    called = None
    dispatcher = AsyncDispatcher(multi=True)

    @dispatcher.register('foo1')
    async def foo1():
        await asyncio.sleep(0.5)
        nonlocal called
        called = 'foo1'
        return 1

    @dispatcher.register('foo1')
    async def foo2():
        nonlocal called
        called = 'foo2'
        return 2

    assert called is None
    ret = await dispatcher.send('foo1')
    assert ret == [1, 2]

    ret = await dispatcher.send('foo3')
    assert ret == []
