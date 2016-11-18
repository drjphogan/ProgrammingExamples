from socket import socket, AF_INET, SOCK_STREAM

from func_tools import functors
from func_tools import persistables
from func_tools.factory import Factory
from func_tools import stream

class FunctorClient(object):

    def __init__(self, ip, port, functor_name):

        self._ip = ip
        self._port = port
        self._functor = Factory().make(functor_name)()

    def __call__(self, params):

        out_stream = stream.TTCompatibleStream()
        in_stream = stream.TTCompatibleStream()

        stream.write_persistable_name(type(self._functor).__name__, out_stream)
        stream.write_persistable(params, out_stream)

        try:

            s = socket(AF_INET, SOCK_STREAM)

            # open socket connection to server
            s.connect((self._ip, self._port))

            # send functor request to server
            out_stream.send(s)

            # receive results from server
            in_stream.recv(s)

            result = stream.read_persistable(in_stream)

        except Exception as e:

            result = persistables.PersistableString(str(e))

        finally:

            s.close()

        return result

    def create_params(self, args):

        return self._functor.create_params_from_args(args)
