import sqlite3


class Db:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = sqlite3.connect('db.sqlite3', isolation_level=None, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.db.execute('DROP TABLE IF EXISTS NICKNAME')
        self.db.execute('DROP TABLE IF EXISTS PLAYER')

    def create_table(self):
        self.db.execute(
            'CREATE TABLE NICKNAME (PK INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, NICKNAME TEXT NOT NULL, ID INTEGER NOT NULL)'
        )
        self.db.execute('''
            CREATE TABLE PLAYER (
                PK INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ROLE INTEGER,
                CHARACTER INTEGER,
                LIFE INTEGER,
                NICKNAME_ID INTEGER
                FOREIGN KEY (NICKNAME_ID) REFERENCES NICKNAME(PK))
            ''')

    def start(self):
        self.connect()
        self.create_table()

    def check_duplicated_nickname(self, nickname):
        self.cursor.execute('SELECT COUNT(*) AS COUNT FROM NICKNAME WHERE NICKNAME = ?', (nickname,))
        # {"code": 111, "nickname": "test"}

        if self.cursor.fetchone()[0] == 0:
            return False

        else:
            return True

    def check_duplicated_id(self, id):
        self.cursor.execute('SELECT COUNT(*) AS COUNT FROM NICKNAME WHERE ID = ?', (id,))
        # {"code": 111, "nickname": "test"}

        if self.cursor.fetchone()[0] == 0:
            return False

        else:
            return True

    def set_nickname(self, nickname, id):
        self.db.execute('INSERT INTO NICKNAME (NICKNAME, ID) VALUES (?, ?)', (nickname, id))
        self.cursor.execute('SELECT * FROM NICKNAME')
        players = []

        for row in self.cursor.fetchall():
            players.append({'nickname': row[1], 'id': row[2]})

        return players

    def delete_nickname(self, id):
        self.db.execute('DELETE FROM NICKNAME WHERE ID = ?', (id,))

    def close(self):
        self.db.close()
