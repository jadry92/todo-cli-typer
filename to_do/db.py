"""
    This module contains the Database class that is used to interact with the
"""
# libraries
import os
import sqlite3

# local
from to_do import DB_ERROR, SUCCESS, console


class Database:
    """sqlite3 database class that contains the To Do"""

    __db_location = os.path.join(os.path.dirname(__file__), "to_do.db")
    __schema_location = os.path.join(os.path.dirname(__file__), "schema.sql")

    def __init__(self, path_db=None):
        if path_db is not None:
            self.__db_connection = sqlite3.connect(
                path_db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
        else:
            self.__db_connection = sqlite3.connect(
                self.__db_location,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
        self.__db_connection.row_factory = sqlite3.Row
        self.cursor = self.__db_connection.cursor()

    def __del__(self):
        self.__db_connection.close()

    def query(self, sql, data=None, all_data=True):
        """
        Execute a query and return the all results or single result
        all_data = True: return all results
        all_data = False: return single result
        """

        if data is not None:
            self.cursor.execute(sql, data)
        else:
            self.cursor.execute(sql)

        if all_data:
            return self.cursor.fetchall()

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
            console.log(
                f":sad_but_relieved_face: Error: {error} :sad_but_relieved_face:",
                style="danger",
            )
            return DB_ERROR

    def insert_many(self, sql, data):
        """
        Execute insert many rows in to the database
        """
        self.cursor.executemany(sql, data)
        return self.cursor.rowcount

    def execute(self, sql):
        """
        Execute sql statement
        """
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
        with open(self.__schema_location, "r", encoding="utf-8") as f:
            self.cursor.executescript(f.read())

    def commit(self):
        """commit changes to database"""
        self.__db_connection.commit()
