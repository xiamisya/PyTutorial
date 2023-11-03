import mariadb
import sys

from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


class Database:
    def __init__(self):
        config = Config("Conf/.db")
        self._conn = mariadb.connect(
            host=config("DATABASE_URL", cast=str, default="postgresql://"),
            user=config("DATABASE_USER", cast=str, default="guest"),
            password=config("DATABASE_PWD", cast=str, default=""),
            db=config("DATABASE_NAME", cast=str, default=""),
            port=3306)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.execute(sql, params or ())
        return self.fetchall()
