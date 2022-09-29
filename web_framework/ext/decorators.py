from datetime import datetime
from sqlite3 import connect
from typing import Callable, Any, Type

from web_framework.database.base import Mapper


def debug(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start = datetime.now()
        result = func(args, **kwargs)
        end = datetime.now() - start
        msg = f'DEBUG: function name: {func.__name__}, working time: {end}'
        print("\033[1m\033[34m{}\033[0m".format(msg))
        return result
    return wrapper


def register_model(cls: Type):
    conn = connect('database.sqlite3')
    mapper = Mapper(cls, conn)
    mapper.create_table()
    return cls
