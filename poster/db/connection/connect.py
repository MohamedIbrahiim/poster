"""
file to create connection and create execute function which will try
to execute database query after opening temporary
connection which must expire after 200 ms
to reduce cost issues in serverless and for performance enhancements
"""
import os
import psycopg2
from poster.db.connection.validators import validate_keys, validate_not_none

__DB_SETTINGS__: dict = {
    "host": os.environ.get("HOST", None),
    "port": os.environ.get("PORT", None),
    "database": os.environ.get("DATABASE", None),
    "user": os.environ.get("USER", None),
    "password": os.environ.get("PASSWORD", None),
}


def set_db_object(connection_obj: dict) -> None:
    """
    function will change DB_SETTINGS to hold user connection details
    :param connection_obj: will hold user connection details in dict
    :return:
    """
    global __DB_SETTINGS__
    __DB_SETTINGS__ = connection_obj
    validate_keys(__DB_SETTINGS__)


class DbConnection:
    @classmethod
    def db_execute(cls, query, params=None, is_commit=False) -> psycopg2:
        """
        function will execute created query and will allow if any modifications
        will happen inside cursor
        :param params:
        :param query: query needs to be executed
        :param is_commit: if allowing to write on database
        :return: returning cursor which will hold data returned from database
        """
        if params is None:
            params = {}
        validate_not_none(__DB_SETTINGS__)
        connection = psycopg2.connect(**__DB_SETTINGS__)
        cursor = connection.cursor()
        cursor.execute(query, params)
        if is_commit:
            connection.commit()
        return cursor
