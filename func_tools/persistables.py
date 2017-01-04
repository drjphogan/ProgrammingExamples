class PersistableBase:

    def save_name_on(self, out_stream):
        out_stream.save_string(self.__class__.__name__)


class PersistableInt(PersistableBase):

    def __init__(self, arg=0):
        self.value = arg

    def create_from_args(self, arg):
        self.value = int(arg)
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_numeric(self.value, 'i')

    def restore_contents_from(self, in_stream):
        self.value = in_stream.restore_numeric('i')

    def __str__(self):
        return str(self.value)


class PersistableFloat(PersistableBase):

    def __init__(self, arg=0.0):
        self.value = arg

    def create_from_args(self, arg):
        self.value = float(arg)
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_numeric(self.value, 'd')

    def restore_contents_from(self, in_stream):
        self.value = in_stream.store_numeric('d')

    def __str__(self):
        return str(self.value)


class PersistableString(PersistableBase):

    def __init__(self, arg=''):
        self.contents = arg

    def create_from_args(self, args):
        self.contents = args
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_string(self.contents)

    def restore_contents_from(self, in_stream):
        self.contents = in_stream.restore_string()

    def __str__(self):
        return str(self.contents)


class PersistableIntVector(PersistableBase):

    def __init__(self, args=[]):
        self.contents = args

    def create_from_args(self, args):
        self.contents = [int(arg) for arg in args]
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_numeric_array(self.contents, 'i')

    def restore_contents_from(self, in_stream):
        self.contents = in_stream.restore_numeric_array('i')

    def __str__(self):
        return str(self.contents)


class PersistableFloatVector(PersistableBase):

    def __init__(self, args=[]):
        self.contents = args

    def create_from_args(self, args):
        self.contents = [float(arg) for arg in args]
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_numeric_array(self.contents, 'd')

    def restore_contents_from(self, in_stream):
        self.contents = in_stream.restore_numeric_array('d')

    def __str__(self):
        return str(self.contents)


class PersistableStringVector(PersistableBase):

    def __init__(self, args=[]):
        self.contents = args

    def create_from_args(self, args):
        self.contents = args
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_string_array(self.contents)

    def restore_contents_from(self, in_stream):
        self.contents = in_stream.restore_string_array()

    def __str__(self):
        return str(self.contents)


class PersistableStudent(PersistableBase):

    def __init__(self):
        self.first_name = ''
        self.second_name = ''
        self.age = -1

    def create_from_args(self, args):
        self.first_name = args[0]
        self.second_name = args[1]
        self.age = int(args[2])
        return self

    def save_contents_on(self, out_stream):
        out_stream.save_string(self.first_name)
        out_stream.save_string(self.second_name)
        out_stream.save_numeric(self.age, 'i')

    def restore_contents_from(self, in_stream):
        self.first_name = in_stream.restore_string()
        self.second_name = in_stream.restore_string()
        self.age = in_stream.restore_numeric('i')

    def __str__(self):
        return str(self.first_name, self.second_name, str(self.age))
