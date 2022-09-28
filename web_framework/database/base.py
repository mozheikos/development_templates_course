import threading
from sqlite3 import Connection, connect
from typing import Any

from web_framework.database.types import Field


class Mapper:

    def __init__(self, obj, connection: Connection):
        self.obj = obj
        self.connection = connection
        self.__tablename__ = obj.__tablename__
        self.fields = []
        self.pk_field = None
        for k, v in obj.__dict__.items():
            if not isinstance(v, Field):
                continue
            if v.primary_key:
                self.pk_field = k
            self.fields.append((k, v))

    def create_table(self):
        fields = []
        for k, v in self.fields:
            row = f"{k} {v.field}"
            if v.primary_key:
                row += ' PRIMARY KEY AUTOINCREMENT UNIQUE'
            else:
                if not v.nullable:
                    row += ' NOT NULL'
                if v.unique:
                    row += ' UNIQUE'
            fields.append(row)

        sql = f"""CREATE TABLE IF NOT EXISTS {self.__tablename__} ({', '.join(fields)})"""

        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def get_all(self):
        sql = f"SELECT * FROM {self.__tablename__}"
        cursor = self.connection.cursor()
        return [self.obj(*x) for x in cursor.execute(sql).fetchall()]

    def filter(self, field: str, value: Any):
        sql = f"SELECT * FROM {self.__tablename__} WHERE {self.__tablename__}.{field}=?"
        cursor = self.connection.cursor()
        return [self.obj(*x) for x in cursor.execute(sql, (value, )).fetchall()]

    def get(self, pk: int):
        sql = f"SELECT * FROM {self.__tablename__} WHERE {self.pk_field}=?"

        cursor = self.connection.cursor()
        result = cursor.execute(sql, (pk,)).fetchone()
        return self.obj(*result) if result else result

    def update(self, obj):

        kwargs = []
        for k, v in obj.__dict__.items():
            if k in self.obj.__dict__.keys() and k != 'id':
                if isinstance(v, str):
                    row = f"{k}='{v}'"
                elif v is None:
                    row = f"{k}=NULL"
                else:
                    row = f"{k}={v}"
                kwargs.append(row)

        update = ', '.join(kwargs)
        sql = f"UPDATE {self.__tablename__} SET {update} WHERE id=?"
        cursor = self.connection.cursor()
        return cursor.execute(sql, (obj.id,))

    def delete(self, obj):
        sql = f"DELETE FROM {self.__tablename__} WHERE id=?"
        cursor = self.connection.cursor()
        return cursor.execute(sql, (obj.id,))

    def create(self, obj):
        fields = [x[0] for x in self.fields if x[0] != 'id']
        inputs = ', '.join(['?' for _ in range(len(self.fields) - 1)])
        sql = f"INSERT INTO {self.__tablename__} {tuple(fields)} VALUES({inputs})"
        cursor = self.connection.cursor()
        return cursor.execute(sql, tuple(v for k, v in obj.__dict__.items() if k in fields)).lastrowid


class Objects:

    current = threading.local()

    def __init__(self):
        self.connection = connect('database.sqlite3')
        self.new = []
        self.updated = set()
        self.removed = set()
        self.set_current(self)

    def __del__(self):
        self.connection.close()
        self.set_current(None)

    @classmethod
    def set_current(cls, obj):
        cls.current.session = obj

    @classmethod
    def get_current(cls):
        return cls.current.session

    def create(self, obj):
        self.new.append(obj)
        return obj

    def update(self, obj):
        self.updated.add(obj)
        return obj

    def remove(self, obj):
        self.removed.add(obj)

    def filter(self, obj, field: str, value: Any):
        mapper = Mapper(obj, self.connection)
        return mapper.filter(field, value)

    def get_by_id(self, obj, pk: int):
        mapper = Mapper(obj, self.connection)
        return mapper.get(pk)

    def get_list(self, obj):
        mapper = Mapper(obj, self.connection)
        return mapper.get_all()

    def commit(self):

        for obj in self.new:
            mapper = Mapper(obj.__class__, self.connection)
            obj.id = mapper.create(obj)

        self.new.clear()

        for obj in self.updated:
            mapper = Mapper(obj.__class__, self.connection)
            mapper.update(obj)

        self.updated.clear()

        for obj in self.removed:
            mapper = Mapper(obj.__class__, self.connection)
            mapper.delete(obj)

        self.removed.clear()

        self.connection.commit()
