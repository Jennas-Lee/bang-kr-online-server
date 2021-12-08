import socket
import threading
import json


def send(client_sock):
    while True:
        send_data = bytes(input().encode())
        client_sock.send(send_data)


def recv(client_sock):
    while True:
        recv_data = client_sock.recv(1024).decode()
        recv_json = json.loads(recv_data)
        code = recv_json.get('code')

        if code == 1:
            print('connection successful')

        elif code == 91:
            print('connection reject')
            client_sock.close()
            exit(0)

        else:
            print(recv_data)


if __name__ == '__main__':
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 5555
    client_sock.connect((host, port))
    print('Connecting to', host, port)

    thread1 = threading.Thread(target=send, args=(client_sock,))
    thread1.start()

    thread2 = threading.Thread(target=recv, args=(client_sock,))
    thread2.start()
