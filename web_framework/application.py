"""
Module define main framework handler class
"""
from typing import Callable, Any, Dict, List, Tuple

from web_framework.ext.exceptions import PathAlreadyRegistered
from web_framework.ext.middleware import fine_path, get_params
from web_framework.ext.responses import HTMLResponse
from web_framework.ext.status import Status


class App:
    """
    Application. In server must be only one instance of application, so
    use 'Singleton' pattern
    """
    __instance = None
    __router = {}
    __middleware = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.middleware_register([get_params, fine_path])

    @classmethod
    def path_register(cls, urls: List[Tuple[str, Callable]]):
        """
        Add item of path - handler to router
        :return:
        """
        for url in urls:
            url_path, handler = url
            if url_path in cls.__router.keys():
                raise PathAlreadyRegistered(url_path)

            cls.__router[url_path] = handler

    @classmethod
    def middleware_register(cls, middleware: List[Callable]):
        """
        Add middleware to list
        :param middleware: Callable
        :return:
        """
        cls.__middleware.extend(middleware)

    @staticmethod
    def not_found(request: dict) -> HTMLResponse:
        return HTMLResponse(body=f'Page {request.get("PATH_INFO")} not found', status=Status.HTTP_404_NOT_FOUND)

    def __call__(self, request: Dict[str, Any], start_response: Callable, *args, **kwargs) -> List[bytes]:
        """
        Application request handler
        :param environ:
        :param start_response:
        :param args:
        :param kwargs:
        :return:
        """
        for middleware in self.__middleware:
            middleware(request)

        path = request.get('PATH_INFO', None)
        handler = self.__router.get(path, self.not_found)

        response = handler(request)
        start_response(response.status_code.value, response.headers)
        return [response.body]
