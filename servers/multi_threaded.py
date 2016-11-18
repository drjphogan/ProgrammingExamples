"""

Implementation of multi thread server using requests

"""
from sys import argv
from socketserver import TCPServer
from threading import Thread
from handlers import request_handler


def main(port):
    print('starting server...')
    nworkers = 16
    serv = TCPServer(('', port), request_handler.FunctorRequestHandler)
    for n in range(nworkers):
        t = Thread(target=serv.serve_forever)
        t.deamon = True
        t.start()
    serv.serve_forever()

if __name__ == '__main__':
    main(int(argv[1]))
