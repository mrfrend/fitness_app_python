from database import Database

class BaseDAO:
    def __init__(self, db: Database):
        self.db = db