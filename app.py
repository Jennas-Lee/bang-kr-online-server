from server.server import Server


def app():
    server = Server()

    try:
        server.open()
        server.run()

    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    app()
