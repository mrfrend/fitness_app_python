from app.core.dao import BaseDAO
from app.database import db

class DirectorDAO(BaseDAO):
    def get_all(self):
        with self.db.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM director")
            return cursor.fetchall()

director_dao = DirectorDAO(db)