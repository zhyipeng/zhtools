from unittest import TestCase

from zhtools.ctx import defer, defer_ctx, recover


class TestDefer(TestCase):

    def test_defer(self):
        data = []

        @defer_ctx
        def foo():
            data.append(1)
            defer(lambda x: data.append(x), -1)
            data.append(2)
            return True

        ret = foo()
        self.assertTrue(ret)
        self.assertEqual(data, [1, 2, -1])

    def test_defer_where_main_function_raise_exception(self):
        data = []

        @defer_ctx
        def foo():
            defer(lambda: data.append(-1))
            data.append(1 / 0)
            data.append(2)

        self.assertRaises(ZeroDivisionError, foo)
        self.assertEqual(data, [-1])

    def test_defer_where_main_function_raise_exception_and_recover(self):
        data = []

        @defer_ctx
        def foo():
            defer(lambda: data.append(recover()))
            data.append(1 / 0)
            data.append(2)
            return True

        ret = foo()
        self.assertIsNone(ret)
        self.assertEqual(len(data), 1)
        self.assertTrue(isinstance(data[0], ZeroDivisionError))

    def test_defer_where_callback_raise_exception(self):
        data = []

        @defer_ctx
        def foo():
            defer(lambda: 1 / 0)
            data.append(1)
            return True

        self.assertRaises(ZeroDivisionError, foo)
        self.assertEqual(data, [1])

    def test_defer_without_ctx(self):
        data = []

        def foo():
            defer(lambda: data.append(1))

        self.assertRaises(AssertionError, foo)
