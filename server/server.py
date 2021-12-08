import json
import sqlite3
import re

from socket import *
from queue import Queue
from threading import Thread

from server.db import Db

HOST = ''
PORT = 5555
BUFFER = 1024


class Server:

    def __init__(self):
        self.sock = None
        self.conn_count = 0
        self.conn_group = []
        self.queue = Queue()
        self.db = Db()

    def open(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        self.db.start()

        print('socket is opened at ', HOST, PORT)

    def close(self):
        self.sock.close()
        self.db.close()

        print('socket is closed at ', HOST, PORT)

    def send(self):
        print('Thread send start')

        while True:
            try:
                recv = self.queue.get()
                recv_json = json.loads(recv[0])

                if recv_json['code'] == 11:
                    nickname = recv_json.get('nickname')
                    msg = {
                        'code': 0
                    }

                    if re.match('^[ㄱ-힣a-zA-Z0-9]{1,10}$', nickname) is None:
                        msg['code'] = 92

                    elif self.db.check_duplicated_nickname(nickname):
                        msg['code'] = 93

                    else:
                        try:
                            msg['code'] = 11
                            msg['players'] = self.db.set_nickname(nickname)

                        except sqlite3.Error as e:
                            print(e.args[0])

                    if msg['code']:  # set nickname failed
                        msg = json.dumps(msg)

                        recv[1].send(msg)
                    else:  # set nickname successful
                        pass

                else:
                    recv[1].send('unknown error ! - ' + recv)

                # for conn in self.conn_group:
                #     msg = 'Client' + str(recv[2]) + ' >> ' + str(recv[0])
                #     if recv[1] != conn:
                #         conn.send(bytes(msg.encode()))
                #     else:
                #         pass

            except json.decoder.JSONDecodeError:
                recv[1].send('unknown error ! - ' + recv)

    def recv(self, conn, count):
        print('Thread recv ' + str(count) + ' start')

        while True:
            try:
                data = conn.recv(BUFFER).decode()
                self.queue.put([data, conn, count])

                print('Client', conn.getpeername(), data)

            except ConnectionResetError as e:  # reset connection
                print('Disconnected by', conn.getpeername(), '- player reset connection')
                self.conn_count -= 1

                break

    def connect(self, conn):
        if self.conn_count > 8:  # too many players
            msg = {
                'code': 91
            }
            msg = json.dumps(msg)

            print('Disconnected by', conn.getpeername(), '- full player')

            conn.send(bytes(msg.encode()))
            conn.close()

            self.conn_count -= 1

            return True

        else:
            msg = {
                'code': 1
            }
            msg = json.dumps(msg)

            conn.send(bytes(msg.encode()))

            return False

    def run(self):
        while True:
            self.conn_count += 1
            conn, addr = self.sock.accept()

            if self.connect(conn):  # reject connection
                pass

            else:  # allow connection
                self.conn_group.append(conn)

                print('Connected by', str(addr), 'at', self.conn_count)

                send_thread = Thread(target=self.send)
                send_thread.start()

                recv_thread = Thread(target=self.recv, args=(conn, self.conn_count))
                recv_thread.start()
