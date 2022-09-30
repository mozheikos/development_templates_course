"""Module for logger"""
import datetime
from typing import Dict, List

from web_framework.ext.exceptions import PathNotSpecified


class SimpleLogger:

    def __init__(self):
        self.name = None
        self.time_format = None

    def _get_message(self, msg: str) -> str:
        """Format message"""
        return f"\n{self.name} - {datetime.datetime.now().strftime(self.time_format)} - {msg}"

    def log(self, text: str):
        raise NotImplementedError


class FileLogger(SimpleLogger):
    """File logger"""
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def log(self, text: str):
        """Log text"""
        if not self.path:
            raise PathNotSpecified("Please specify path of file by calling set_path(path: str)")

        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(self._get_message(text))


class ConsoleLogger(SimpleLogger):

    def log(self, text: str):
        print(self._get_message(text))


class LoggerItem:

    time_format = '%Y-%m-%d %H:%M:%S'

    __loggers: List[SimpleLogger] = []

    def __init__(self, name: str):
        self.name = name

    def add_logger(self, logger):
        logger.name = self.name
        logger.time_format = self.time_format
        self.__loggers.append(logger)

    def log(self, text: str):
        for logger in self.__loggers:
            logger.log(text)


class Logger:
    __loggers: Dict[str, LoggerItem] = {}

    @classmethod
    def get_logger(cls, name: str) -> LoggerItem:
        logger = cls.__loggers.get(name, None)

        if not logger:
            logger = LoggerItem(name)
        return logger
