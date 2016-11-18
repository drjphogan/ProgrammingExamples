from threading import Thread
from socketserver import TCPServer
from handlers import request_handler


class FunctorRequestServer(object):

    def __init__(self, port):
        self._port = port
        self._server = TCPServer(('', self._port), request_handler.FunctorRequestHandler)
        self._t = Thread(target=self._server.serve_forever)

    def start(self):
        print('Starting request server on port ', self._port)
        self._t.start()


def main():

    fs1 = FunctorRequestServer(20000)
    fs2 = FunctorRequestServer(20001)
    fs1.start()
    fs2.start()

if __name__ == "__main__":
    main()
