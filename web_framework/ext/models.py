"""Module with data models"""

from web_framework.database.base import Objects
from web_framework.database.types import Field


class Model:

    __tablename__ = ''

    def __init__(self, pk: int = None):
        self.id = pk

    def __hash__(self):
        return hash((self.__class__.__tablename__, self.id))

    def dict(self):
        result = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                result[k] = self.__dict__.get(k)
        return result


class Engine:
    """Main engine class"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton realization"""
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.objects = Objects()
