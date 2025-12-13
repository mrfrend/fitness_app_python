import pymysql
from pymysql.cursors import DictCursor

class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=DictCursor)

# Можно менять аргументы, однако изменения в данном файле не коммитить
db = Database("localhost", "root", "", "fitness_app")