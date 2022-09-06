"""
Status codes
"""


from enum import Enum


class Status(str, Enum):
    """
    Enum class defines status
    """
    HTTP_200_OK = '200 OK'
    HTTP_400_BAD_REQUEST = '400 Bad Request'
    HTTP_404_NOT_FOUND = '404 Not Found'
