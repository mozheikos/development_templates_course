from datetime import datetime
from typing import Callable, Any, Type

from web_framework.ext.models import Engine


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

    engine = Engine()
    name = cls.__name__.lower()

    exist = engine.models.objects.get(name, None)
    if not exist:
        engine.models.objects[name] = {}
    return cls
