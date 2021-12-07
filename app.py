from server.main import Main


def app():
    server = Main()
    server.on()


if __name__ == '__main__':
    app()
