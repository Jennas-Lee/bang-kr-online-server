from socket import *

HOST = ''
PORT = 5555
BUFFER = 1024


# sock = socket(AF_INET, SOCK_STREAM)
# sock.bind(('', 5555))
# sock.listen()
#
# client_sock, addr = sock.accept()
#
# print('Connected by', addr)
#
# while True:
#     data = client_sock.recv(1024)
#
#     if not data:
#         break
#
#     print('Received from', addr, data.decode())
#
#     client_sock.sendall(data)
#
# client_sock.close()
# sock.close()

class Main:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((HOST, PORT))

    def on(self):
        self.sock.listen()
