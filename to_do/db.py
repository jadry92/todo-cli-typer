import sqlite3
# local
from to_do import ERROR, DB_ERROR, SUCCESS


class Database():
    """sqlite3 database class that contains the To Do"""
    __DB_LOCATION = "./to_do/to_do.db"
    __SCHEMA_LOCATION = "./to_do/schema.sql"

    def __init__(self, path_db=None):
        if path_db is not None:
            self.__db_connection = sqlite3.connect(
                path_db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        else:
            self.__db_connection = sqlite3.connect(
                self.__DB_LOCATION, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.__db_connection.row_factory = sqlite3.Row
        self.cursor = self.__db_connection.cursor()

    def __del__(self):
        self.__db_connection.close()

    def query(self, sql, data=None, all=True):
        if data is not None:
            self.cursor.execute(sql, data)
        else:
            self.cursor.execute(sql)

        if all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def insert(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.cursor.rowcount
            if self.cursor.rowcount == -1:
                return DB_ERROR
            return SUCCESS
        except sqlite3.OperationalError as Error:
            print(Error.args)
            return DB_ERROR

    def insert_many(self, sql, data):
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
        with open(self.__SCHEMA_LOCATION) as f:
            self.cursor.executescript(f.read())

    def commit(self):
        """commit changes to database"""
        self.__db_connection.commit()
