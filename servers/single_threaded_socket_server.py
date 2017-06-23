"""

Implementation of multi thread server using sockets

"""
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from handlers.socket_handler import socket_connection_handler


class FunctorSocketConnectionServer(object):

    def __init__(self, port, backlog=5):
        self._port = port
        self._backlog = backlog
        self._t = Thread(target=self._run)

    def start(self):
        print('Starting socket server on port c', self._port)
        self._t.start()

    def _run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(('', self._port))
        sock.listen(self._backlog)
        while True:
            client_sock, client_address = sock.accept()
            socket_connection_handler(client_sock, client_address)


def main():

    fs1 = FunctorSocketConnectionServer(20000)
    fs2 = FunctorSocketConnectionServer(20001)
    fs1.start()
    fs2.start()

if __name__ == "__main__":
    main()
