"""Router module"""
from typing import Callable, Optional


class Router:
    """Class-Decorator to route path to controllers"""
    def __init__(self, *,  namespace: str = ''):
        self.__namespace = '/' + namespace
        self.__path: Optional[str] = None
        self.__urls = []

    def _decorator(self, func: Callable) -> Callable:
        path = f"{self.__namespace}{self.__path}"

        url = (path, func)
        self.__urls.append(url)
        return func

    @property
    def urls(self) -> list:
        return self.__urls

    def route(self, path: str) -> Callable:
        if not path.startswith('/'):
            path = '/' + path

        if not path.endswith('/'):
            path += '/'

        self.__path = path
        return self._decorator
