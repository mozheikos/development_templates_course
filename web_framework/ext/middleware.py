"""
Middleware module
"""
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


def get_params(request: Dict[str, Any]):
    """
    Get path params from request
    :param request: dict
    :return:
    """

    params = request.get('QUERY_STRING', '').split('&')
    if '' in params:
        params.remove('')
    for param in params:
        key, value = param.split('=')
        request[key] = value
