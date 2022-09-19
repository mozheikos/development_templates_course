"""
Module define responses class
"""
import json
from typing import Tuple, List, Union, Optional

from config import STATIC_PATH
from web_framework.ext.exceptions import BodyEncodingError
from web_framework.ext.status import Status


class Response:
    """
    Response base class
    """

    def __init__(self, body: Union[str, list, dict] = '', status: Status = Status.HTTP_200_OK):
        self.status_code: Optional[Status] = None
        self.headers: List[Tuple[str, str]] = []
        self.body = None
        self.set_body(body)
        self.set_status_code(status)

    @classmethod
    def encode_body(cls, body: str) -> bytes:
        if cls.__name__ == 'StaticResponse':
            with open(body, 'rb') as f:
                return f.read()

        try:
            result = bytes(body, encoding='unicode-escape')
        except Exception:
            raise BodyEncodingError('Encoding error')
        return result

    def add_headers(self, headers: List[Tuple[str, str]]):
        """
        Add headers
        :param headers: List[Tuple]
        :return:
        """
        self.headers.extend(headers)

    def set_body(self, value: Union[str, dict]):
        """
        Set body to class property
        :param value: str
        :return:
        """
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        self.body = self.encode_body(value)

    def set_status_code(self, status: Status):
        """
        Set status code
        :param status: Status
        :return:
        """
        self.status_code = status


class HTMLResponse(Response):
    """
    HTML Response
    """

    def __init__(self, body: str = '', status: Status = Status.HTTP_200_OK):
        """
        Init
        :param body:
        :param status:
        """
        body = ''.join(body.split('\n'))
        super(HTMLResponse, self).__init__(body=body, status=status)
        self.add_headers([('Content-type', 'text/html')])


class JSONResponse(Response):
    """
    Implementation of JSON Response
    """

    def __init__(self, body: Union[list, dict], status: Status = Status.HTTP_200_OK):
        """
        Init
        :param body:
        :param status:
        """
        super(JSONResponse, self).__init__(body=body, status=status)
        self.add_headers([('Content-type', 'application/json'), ('Content-length', str(len(self.body)))])


class StaticResponse(Response):
    """
    Static response
    """
    def __init__(self, path: str, kind: str):
        """Init. Get file and return Response"""
        super(StaticResponse, self).__init__(body=path, status=Status.HTTP_200_OK)
        self.add_headers([('Content-type', kind)])
