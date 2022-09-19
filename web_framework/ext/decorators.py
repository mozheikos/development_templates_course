from datetime import datetime
from typing import Callable, Any


def debug(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start = datetime.now()
        result = func(args, **kwargs)
        end = datetime.now() - start
        msg = f'DEBUG: function name: {func.__name__}, working time: {end}'
        print("\033[1m\033[34m{}\033[0m".format(msg))
        return result
    return wrapper
