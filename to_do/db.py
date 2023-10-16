"""
    This module contains the Database class that is used to interact with the
"""

import sqlite3

# local
from to_do import DB_ERROR, SUCCESS


class Database:
    """sqlite3 database class that contains the To Do"""

    __DB_LOCATION = "./to_do/to_do.db"
    __SCHEMA_LOCATION = "./to_do/schema.sql"

    def __init__(self, path_db=None):
        if path_db is not None:
            self.__db_connection = sqlite3.connect(
                path_db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
        else:
            self.__db_connection = sqlite3.connect(
                self.__DB_LOCATION,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
        self.__db_connection.row_factory = sqlite3.Row
        self.cursor = self.__db_connection.cursor()

    def __del__(self):
        self.__db_connection.close()

    def query(self, sql, data=None, all_data=True):
        """
        Execute a query and return the all results or single result
        all = True: return all results
        all = False: return single result
        """

        if data is not None:
            self.cursor.execute(sql, data)
        else:
            self.cursor.execute(sql)

        if all_data:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def insert(self, sql, data):
        """
        Execute insert a single row in to the database
        """
        try:
            self.cursor.execute(sql, data)
            if self.cursor.rowcount == -1:
                return DB_ERROR
            return SUCCESS
        except sqlite3.OperationalError as error:
            print(error.args)
            return DB_ERROR

    def insert_many(self, sql, data):
        """
        Execute insert many rows in to the database
        """
        self.cursor.executemany(sql, data)
        return self.cursor.rowcount

    def execute(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.rowcount
        if result == -1:
            return DB_ERROR
        else:
            return SUCCESS

    def create_schema(self):
        """
        Create the schema of the database
        base on the schema.sql file
        """
        with open(self.__SCHEMA_LOCATION) as f:
            self.cursor.executescript(f.read())

    def commit(self):
        """commit changes to database"""
        self.__db_connection.commit()
