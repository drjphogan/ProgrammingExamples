"""

Implementation of multi thread server

"""
from sys import argv
from socketserver import TCPServer
from threading import Thread
from handlers import request_handler


def main(port):
    print('starting multi-threaded server...')
    nworkers = 16
    TCPServer.allow_reuse_address = True
    serv = TCPServer(('', port), request_handler.FunctorRequestHandler)
    for n in range(nworkers):
        t = Thread(target=serv.serve_forever)
        t.deamon = True
        t.start()
    serv.serve_forever()

if __name__ == '__main__':
    main(int(argv[1]))
