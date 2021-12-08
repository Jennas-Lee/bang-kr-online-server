import sqlite3


class Db:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = sqlite3.connect('db.sqlite3', isolation_level=None)
        self.cursor = self.db.cursor()
        self.db.execute('DROP TABLE IF EXISTS NICKNAME')

    def create_table(self):
        self.db.execute(
            'CREATE TABLE NICKNAME (PK INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, NICKNAME TEXT NOT NULL, ID INTEGER NOT NULL)'
        )

    def start(self):
        self.connect()
        self.create_table()

    def check_duplicated_nickname(self, nickname):
        self.cursor.execute('SELECT COUNT(*) FROM NICKNAME WHERE NICKNAME = %s', (nickname,))

        print(self.cursor.fetchone())

    def set_nickname(self, nickname, id):
        self.db.execute('INSERT INTO NICKNAME (NICKNAME, ID) VALUES (%s)', (nickname, id))
        self.cursor.execute('SELECT * FROM NICKNAME')

        for row in self.cursor.fetchall():
            print(row)

    def delete_nickname(self, id):
        self.db.execute('DELETE FROM NICKNAME WHERE ID = %s', (id,))

    def close(self):
        self.db.close()
