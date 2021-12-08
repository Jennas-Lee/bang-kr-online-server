import json
import traceback

from socket import *
from queue import Queue
from threading import Thread

from game.db import Db
from game.nickname import set_nickname
from game.start import start_game

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
            msg = {'code': 0}

            try:
                recv = self.queue.get()
                recv_json = json.loads(recv[0])

                if recv_json.get('code') == 111:  # set nickname
                    msg = set_nickname(recv_json.get('nickname'), recv[2], self.db)

                elif recv_json.get('code') == 121:  # start game
                    msg = start_game(self.db)

                else:
                    msg['code'] = 298
                    print('unknown error ! - ' + recv[0])

            except json.decoder.JSONDecodeError:
                msg['code'] = 298
                print('unknown error ! - ' + recv[0])

            except Exception as e:
                msg['code'] = 299
                print(e.args[0])
                traceback.print_exc()

            msg = json.dumps(msg)
            recv[1].send(bytes(msg.encode()))

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
                'code': 291
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
