"""Module for logger"""
import datetime
from typing import Dict

from web_framework.ext.exceptions import PathNotSpecified


class LoggerItem:

    time_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, name: str):
        self.name = name
        self.path = None

    def set_path(self, path: str):
        """Set path of file where log write"""
        self.path = path

    def log(self, text: str):
        """Log text"""
        if not self.path:
            raise PathNotSpecified("Please specify path of file by calling set_path(path: str)")
        output = f"{self.name} - {datetime.datetime.now().strftime(self.time_format)} - {text}"
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(output)
        print(output)


class Logger:
    __loggers: Dict[str, LoggerItem] = {}

    @classmethod
    def get_logger(cls, name: str) -> LoggerItem:
        logger = cls.__loggers.get(name, None)

        if not logger:
            logger = LoggerItem(name)
        return logger
