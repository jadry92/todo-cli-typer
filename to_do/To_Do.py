from datetime import datetime
from typing import List
from to_do.db import Database
from to_do import DB_ERROR, DATA_ERROR, SUCCESS


class ToDo():
    def __init__(self) -> None:
        self.db = Database()
        self.id = None
        self.name = None
        self.done_by = None
        self.created = datetime.now()
        self.done = False

    def _validate_data(self) -> int:
        if self.done_by is not None:
            if self.created > self.done_by:
                return DATA_ERROR
        return SUCCESS

    def create(self, name: str, done_by: datetime):
        self.id = None
        self.name = name
        self.done_by = done_by
        self.created = datetime.now()
        self.done = False
        result = self._validate_data()
        if result == DATA_ERROR:
            return DATA_ERROR

        sql = """
        INSERT INTO to_do (name, date, done_by, done)
        VALUES(?, ?, ?, ?);
        """
        data = (
            self.name,
            self.created,
            self.done_by,
            self.done
        )

        result = self.db.insert(sql, data)
        if result == SUCCESS:
            self.id = self.db.cursor.lastrowid

        return result

    def save(self):
        self.db.commit()

    def delete(self, todo_id) -> int:
        return self.db.execute(f"DELETE FROM to_do WHERE id = {todo_id};")

    def update(self, todo_id, *args, **kwargs) -> int:
        values = []
        if kwargs:
            for key in kwargs.keys():
                values.append(f"{key} = '{kwargs[key]}'")

        sql = f"UPDATE to_do SET {','.join(values)} WHERE id = {todo_id};"
        return self.db.execute(sql)

    def one(self, todo_id: int):
        return self.db.query(f"SELECT * FROM to_do WHERE id = {todo_id}", all=False)

    def all(self):
        return self.db.query("SELECT * FROM to_do ORDER BY done_by", all=True)

    def init_db(self):
        self.db.create_schema()
        self.db.commit()
        return SUCCESS

    def filter(self, patter: str = ''):
        if patter == '':
            return DATA_ERROR
        sql = f"SELECT * FROM to_do WHERE {patter}"
        return self.db.query(sql, all=True)
