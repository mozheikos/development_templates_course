"""
Middleware module
"""
import json
from quopri import decodestring
from typing import Dict, Any


def fine_path(request: Dict[str, str]):
    """
    Check path and add '/' at the end if needed
    :param request: dict
    :return:
    """
    path = request['PATH_INFO']
    if not path.endswith('/'):
        path += '/'

    request['PATH_INFO'] = path


def decode_value(value: str) -> str:
    """Decode query params"""
    return decodestring(value.replace('%', '=').replace('+', ' ').encode('utf-8')).decode('utf-8')


def get_post_data(request: Dict[str, Any]):
    """
    Get POST body
    :param request:
    :return:
    """
    length = int(request.get('CONTENT_LENGTH', 0))
    request['body'] = {}
    if length:
        for item in request['wsgi.input'].read(length).decode(encoding='unicode-escape').split('&'):
            k, v = item.split('=')
            request['body'][k] = decode_value(v)

    print('POST data:')
    print(json.dumps(request['body'], indent=4, ensure_ascii=False))


def get_params(request: Dict[str, Any]):
    """
    Get path params from request
    :param request: dict
    :return:
    """

    #  В случае POST-запроса выполняется функция получения данных тела запроса именно дополнительно к
    #  функции получения данных url-параметров, так как чисто технически пост запрос может иметь
    #  параметры в адресной строке (хотя так и не делают, но физически это возможно)
    method = request.get('REQUEST_METHOD', None).lower()
    if method == 'post':
        get_post_data(request)

    print(f'Method: {method}')

    params = request.get('QUERY_STRING', '').split('&')
    request['params'] = {}
    if '' in params:
        params.remove('')

    for param in params:
        key, value = param.split('=')
        request['params'][key] = decode_value(value)

    request['method'] = method
    print('URL params:')
    print(json.dumps(request['params'], indent=4, ensure_ascii=False))
