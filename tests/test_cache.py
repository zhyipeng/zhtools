from unittest import TestCase

from zhtools.cache import cache


called_times = 0


@cache(key_prefix='test')
def simple_cache():
    global called_times
    called_times += 1
    return called_times


called = False


@cache(key_prefix='test1')
def cache_with_params(a: int, b: int):
    global called
    called = True
    return a + b


called2 = False


@cache(key_prefix='test2')
def cache_with_ignore_exception(a, b):
    global called2
    called2 = True
    return a / b


called3 = False


@cache(key_prefix='test3', ignore_exception=False)
def cache_with_exception(a, b):
    global called3
    called3 = True
    return a / b


@cache(key_prefix='test4')
def cache1():
    return 1


class TestCache(TestCase):

    def test_use_cache(self):
        self.assertEqual(called_times, 0)
        ret = simple_cache()
        self.assertEqual(called_times, 1)
        self.assertEqual(ret, 1)
        simple_cache()
        self.assertEqual(called_times, 1)
        self.assertEqual(ret, 1)

    def test_use_cache_with_params(self):
        global called
        ret = cache_with_params(1, 2)
        self.assertEqual(ret, 3)
        self.assertTrue(called)

        called = False
        ret = cache_with_params(1, 2)
        self.assertEqual(ret, 3)
        self.assertFalse(called)

        ret = cache_with_params(2, 2)
        self.assertEqual(ret, 4)
        self.assertTrue(called)

    def test_cache_with_exception(self):
        global called2
        with self.assertRaises(ZeroDivisionError):
            cache_with_ignore_exception(2, 0)

        self.assertTrue(called2)

        called2 = False
        with self.assertRaises(ZeroDivisionError):
            cache_with_ignore_exception(2, 0)

        self.assertTrue(called2)

    def test_cache_with_exception_and_not_ignore(self):
        global called3
        with self.assertRaises(ZeroDivisionError):
            cache_with_exception(2, 0)

        self.assertTrue(called3)

        called3 = False
        with self.assertRaises(ZeroDivisionError):
            cache_with_exception(2, 0)

        self.assertFalse(called3)

    def test_update_cache_result(self):
        ret = cache1()
        self.assertEqual(ret, 1)
        ret = cache1()
        self.assertEqual(ret, 1)

        cache1.update_cached_result(2)
        ret = cache1()
        self.assertEqual(ret, 2)
