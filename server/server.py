import json

from socket import *
from queue import Queue
from threading import Thread

HOST = ''
PORT = 5555
BUFFER = 1024


class Server:

    def __init__(self):
        self.sock = None
        self.conn_count = 0
        self.conn_group = []
        self.queue = Queue()

    def open(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()

        print('socket is opened at ', HOST, PORT)

    def close(self):
        self.sock.close()

        print('socket is closed at ', HOST, PORT)

    def run(self):
        while True:
            self.conn_count += 1
            conn, addr = self.sock.accept()

            if self.connect(conn):             # reject connection
                pass

            else:                              # allow connection
                self.conn_group.append(conn)

                print('Connected ', str(addr), 'at', self.conn_count)

                send_thread = Thread(target=self.send)
                send_thread.start()

                recv_thread = Thread(target=self.recv, args=(conn, self.conn_count))
                recv_thread.start()

    def send(self):
        print('Thread send start')

        while True:
            try:
                recv = self.queue.get()

                for conn in self.conn_group:
                    msg = 'Client' + str(recv[2]) + ' >> ' + str(recv[0])
                    if recv[1] != conn:
                        conn.send(bytes(msg.encode()))
                    else:
                        pass

            except:
                pass

    def recv(self, conn, count):
        print('Thread recv ' + str(count) + ' start')

        while True:
            data = conn.recv(BUFFER).decode()
            self.queue.put([data, conn, count])

    def connect(self, conn):
        if self.conn_count > 8:
            msg = {
                'code': 91
            }
            msg = json.dumps(msg)

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
