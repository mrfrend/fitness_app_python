from app.database import Database

class BaseDAO:
    def __init__(self, db: Database):
        self.db = db

    def fetch_one(self, query: str, params: tuple | dict | None = None):
        with self.db.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple | dict | None = None):
        with self.db.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute(self, query: str, params: tuple | dict | None = None) -> int:
        with self.db.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def executemany(self, query: str, params_seq: list[tuple] | list[dict]) -> int:
        with self.db.conn.cursor() as cursor:
            cursor.executemany(query, params_seq)
            return cursor.rowcount

    def fetch_scalar(self, query: str, params: tuple | dict | None = None):
        row = self.fetch_one(query, params)
        if row is None:
            return None
        if isinstance(row, dict):
            return next(iter(row.values()), None)
        return row[0]

    def commit(self) -> None:
        self.db.conn.commit()

    def rollback(self) -> None:
        self.db.conn.rollback()