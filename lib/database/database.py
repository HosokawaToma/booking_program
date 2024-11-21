import MySQLdb
from .. import config

class Database():
    def __init__(self):
        self.con = MySQLdb.connect(
            unix_socket = config.DATABASE_SOCKET(),
            user = config.DATABASE_USER(),
            passwd = config.DATABASE_PASSWORD(),
            db = config.DATABASE_NAME(),
            charset = config.database_charset())
        self.cur = self.con.cursor()

    def execute(self, sql):
        self.cur.execute(sql)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()