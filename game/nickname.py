import re
import sqlite3


def set_nickname(nickname, id, db):
    msg = {'code': 0}

    if re.match('^[ㄱ-힣a-zA-Z0-9]{1,10}$', nickname) is None:
        msg['code'] = 292

    elif db.check_duplicated_nickname(nickname):
        msg['code'] = 293

    elif db.check_duplicated_id(id):
        msg['code'] = 294

    else:
        try:
            msg['code'] = 202
            msg['players'] = db.set_nickname(nickname, id)

        except sqlite3.Error as e:
            msg['code'] = 299
            print(e.args[0])
            print(e)

    return msg
