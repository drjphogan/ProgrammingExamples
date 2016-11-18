from sys import argv

from func_tools.factory import Factory
from func_tools.functor_client import FunctorClient
from func_tools import functors
from func_tools import persistables

# register the functors to be remotely executed
Factory().register(functors.Add)
Factory().register(functors.Sub)
Factory().register(functors.Sleep)
Factory().register(functors.IntVectorSummator)
Factory().register(functors.PrintStudent)
Factory().register(functors.Concatenate)

# register the persistable objects used as return variables
Factory().register(persistables.PersistableInt)
Factory().register(persistables.PersistableString)
Factory().register(persistables.PersistableIntVector)
Factory().register(persistables.PersistableStringVector)
Factory().register(persistables.PersistableStudent)


def make_functor_call(ip, port, functor_name, *args):

    fc = FunctorClient(ip, port, functor_name)

    params = fc.create_params(*args)

    result = fc(params)

    return result

def main():
    for i in range(1000):
        result = make_functor_call('localhost', 20000, 'PrintStudent', ['Mark','Day',21])
        print(str(result))

if __name__ == "__main__":
    ip = argv[1]
    port = int(argv[2])
    function = argv[3]
    for i in range(1000):
        result = make_functor_call(ip, port, function, argv[4:])
        print(str(result))
