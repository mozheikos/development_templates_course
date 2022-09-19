"""
Module define main framework handler class
"""
from typing import Callable, Any, Dict, List, Tuple

from config import STATIC_PATH
from web_framework.ext.exceptions import PathAlreadyRegistered
from web_framework.ext.middleware import fine_path, get_params
from web_framework.ext.models import Engine
from web_framework.ext.responses import HTMLResponse, StaticResponse
from web_framework.ext.status import Status


class App:
    """
    Application. In server must be only one instance of application, so
    use 'Singleton' pattern
    """
    __instance = None
    __router = {}
    __middleware = []
    __static_dict = {
            'script': ('js/', 'application/javascript'),
            'style': ('css/', 'text/css')
        }

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.engine = Engine()
        self.middleware_register([get_params, fine_path])
        self.static_path = STATIC_PATH

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

    def static(self, file_type: str, file_name: str) -> StaticResponse:

        folder, header = self.__static_dict.get(file_type)

        path = self.static_path + folder + file_name.strip('/')
        result = StaticResponse(path=path, kind=header)
        return result

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

        request_type = request.get('HTTP_SEC_FETCH_DEST', None)

        path = request.get('PATH_INFO', None)
        if request_type in self.__static_dict.keys():
            response = self.static(request_type, path)
        else:
            handler = self.__router.get(path, self.not_found)

            response = handler(request)
        start_response(response.status_code.value, response.headers)
        return [response.body]
