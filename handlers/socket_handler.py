"""

    Module contains a list of commands that can be executed on server

"""
from threading import current_thread

from func_tools.stream import TTCompatibleStream
from func_tools.functor_server import FunctorServer


def socket_connection_handler(client_socket, client_address):

    print(current_thread().name, 'socket connection received from {}'.format(client_address))

    # Create the input and output streams
    in_stream = TTCompatibleStream()
    out_stream = TTCompatibleStream()

    FunctorServer.process_buffers(client_socket, in_stream, out_stream)

    out_stream.send(client_socket)

    client_socket.close()
