from contextlib import contextmanager

from zhtools.config import config


@contextmanager
def ignore_exception():
    try:
        yield
    except:
        config.log_exception('Exception raise but has been ignored.')
