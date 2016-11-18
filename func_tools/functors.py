from func_tools import persistables as pst
from time import sleep


class Add:

    @staticmethod
    def create_empty():
        return Add()

    def create_params_from_args(self, args):
        return self.params.create_from_args(args)

    def __init__(self):
        self.params_type = pst.PersistableIntVector
        self.params = self.params_type()
        self.result_type = pst.PersistableInt

    def execute(self):
        return self.result_type(self.params.contents[0] + self.params.contents[1])


class Sub:

    @staticmethod
    def create_empty():
        return Sub()

    def create_params_from_args(self, args):
        return self.params.create_from_args(args)

    def __init__(self):
        self.params_type = pst.PersistableIntVector
        self.params = self.params_type()
        self.result_type = pst.PersistableInt

    def execute(self):
        return self.result_type(self.params.contents[0] - self.params.contents[1])


class Sleep:

    @staticmethod
    def create_empty():
        return Sleep()

    def create_params_from_args(self, args):
        return self.params.create_from_args(args)

    def __init__(self):
        self.params_type = pst.PersistableInt
        self.params = self.params_type()
        self.result_type = pst.PersistableString

    def execute(self):
        duration = self.params.value
        sleep(duration)
        msg = ''.join(['Server thread successfully slept for ', str(duration), ' seconds.'])
        return self.result_type(msg)


class IntVectorSummator:

    @staticmethod
    def create_empty():
        return IntVectorSummator()

    def create_params_from_args(self, args):
        return self.params.create_from_args(args)

    def __init__(self):
        self.params_type = pst.PersistableIntVector
        self.params = self.params_type()
        self.result_type = pst.PersistableInt

    def execute(self):
        return self.result_type(sum(self.params.contents))


class Concatenate:

    @staticmethod
    def create_empty():
        return Concatenate()

    def create_params_from_args(self, args):
        return self.params.create_from_args(args)

    def __init__(self):
        self.params_type = pst.PersistableStringVector
        self.params = self.params_type()
        self.result_type = pst.PersistableString

    def execute(self):
        print(type(self.params))
        concatenated_string = ''.join(self.params.contents)
        print(concatenated_string)
        return self.result_type(concatenated_string)


class PrintStudent:

    @staticmethod
    def create_empty():
        return PrintStudent()

    def create_params_from_args(self, args):
        return self.params.create_from_args(args)

    def __init__(self):
        self.params_type = pst.PersistableStudent
        self.params = self.params_type()
        self.result_type = pst.PersistableString

    def execute(self):
        print('Student details received', self.params.first_name, self.params.second_name, self.params.age)
        msg = ''.join(['Student ', self.params.first_name, ' ', self.params.second_name, ' successfully printed.'])
        return self.result_type(msg)
