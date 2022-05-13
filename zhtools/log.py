import logging
from logging.config import dictConfig


class LoggingConfig:

    def __init__(self,
                 log_file: str = 'app.log',
                 level: int = logging.INFO,
                 max_bytes: int = 1 * 1024 * 1024):
        self.log_file = log_file
        self.level = level
        self.max_bytes = max_bytes
        self.formatters = {
            'default': {
                'format': '%(asctime)s[%(levelname)s] %(message)s',
            },
        }
        self.handlers = {
            'default': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': self.log_file,
                'formatter': 'default',
                'level': self.level,
                'maxBytes': self.max_bytes,
            },
        }
        self.loggers = {}

    @property
    def config(self):
        conf = {
            'version': 1,
            'formatters': self.formatters,
            'handlers': self.handlers,
            'root': {
                'level': self.level,
                'handlers': ['default']
            },
        }
        if self.loggers:
            conf['loggers'] = self.loggers
        return conf

    def add_formatter(self, name: str, formatter: dict):
        self.formatters[name] = formatter

    def add_handler(self, name: str, handler: dict):
        self.handlers[name] = handler

    def add_logger(self, name: str, logger: dict):
        self.loggers[name] = logger

    def initial_config(self):
        dictConfig(self.config)


def simple_logging_config(log_file: str = 'app.log', level: int = logging.INFO):
    conf = LoggingConfig(log_file, level)
    conf.initial_config()
