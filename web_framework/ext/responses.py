"""
Module define responses class
"""
import json
from typing import Tuple, List, Union

from web_framework.ext.exceptions import BodyEncodingError
from web_framework.ext.status import Status


class Response:
    """
    Response base class
    """
    status_code: Status = None
    headers: List[Tuple[str, str]] = []
    body: bytes = None

    def __init__(self, body: Union[str, list, dict] = '', status: Status = Status.HTTP_200_OK):
        self.set_body(body)
        self.set_status_code(status)

    @staticmethod
    def encode_body(body: str) -> bytes:
        try:
            result = bytes(body, encoding='unicode-escape')
        except Exception:
            raise BodyEncodingError('Encoding error')
        return result

    @classmethod
    def add_headers(cls, headers: List[Tuple[str, str]]):
        """
        Add headers
        :param headers: List[Tuple]
        :return:
        """
        cls.headers.extend(headers)

    @classmethod
    def set_body(cls, value: Union[str, dict]):
        """
        Set body to class property
        :param value: str
        :return:
        """
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        cls.body = cls.encode_body(value)

    @classmethod
    def set_status_code(cls, status: Status):
        """
        Set status code
        :param status: Status
        :return:
        """
        cls.status_code = status


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
