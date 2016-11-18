"""

    Module contains a list of commands that can be executed on server

"""
from func_tools import functors
from func_tools import persistables
from threading import current_thread

from func_tools import stream
from func_tools.factory import Factory, FactoryError

# register the functions to be remotely executed
Factory().register(functors.Add)
Factory().register(functors.Sub)
Factory().register(functors.Sleep)
Factory().register(functors.IntVectorSummator)
Factory().register(functors.PrintStudent)
Factory().register(functors.Concatenate)

# register the persistable objects used as params variables
Factory().register(persistables.PersistableInt)
Factory().register(persistables.PersistableString)
Factory().register(persistables.PersistableIntVector)
Factory().register(persistables.PersistableStringVector)
Factory().register(persistables.PersistableStudent)


class FunctorServer(object):

    @staticmethod
    def process_buffers(connection, in_stream, out_stream):

        try:

            in_stream.recv(connection)

            functor_type = stream.read_persistable_name(in_stream)

            functor = Factory().make(functor_type)()

            functor.params = stream.read_persistable(in_stream)

            result = functor.execute()

            print(current_thread().name, functor_type, 'functor successfully executed.')

            stream.write_persistable(result, out_stream)

        except FactoryError as e:

            error_msg = ''.join([type(e).__name__, ' On Server: ', str(e)])

            error = persistables.PersistableString(error_msg)

            stream.write_persistable(error, out_stream)
