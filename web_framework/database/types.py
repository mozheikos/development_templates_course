from typing import Type


class TYPE:
    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()


class REAL(TYPE):
    pass


class TEXT(TYPE):
    pass


class INTEGER(TYPE):
    pass


class BLOB(TYPE):
    pass


class Field:

    def __init__(
            self,
            field: Type[TYPE],
            autoincrement: bool = False,
            primary_key: bool = False,
            nullable: bool = True,
            unique: bool = False
    ):
        self.field = field()
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.nullable = nullable
        self.unique = unique

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
