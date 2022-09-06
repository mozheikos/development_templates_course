"""
Module defines custom exceptions
"""


class PathAlreadyRegistered(Exception):
    """Raises when try to register already exists path"""
    pass


class BodyEncodingError(Exception):
    """Raises on errors when encode response body"""
    pass
