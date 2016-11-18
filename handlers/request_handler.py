"""

    Module contains a list of commands that can be executed on server

"""
from socketserver import BaseRequestHandler
from threading import current_thread

from func_tools.stream import TTCompatibleStream
from func_tools.functor_server import FunctorServer


class FunctorRequestHandler(BaseRequestHandler):

    def handle(self):

        print(current_thread().name, 'request received from', self.client_address)

        # Create the input and output streams
        in_stream = TTCompatibleStream()
        out_stream = TTCompatibleStream()

        FunctorServer.process_buffers(self.request, in_stream, out_stream)

        out_stream.send(self.request)

        self.finish()
