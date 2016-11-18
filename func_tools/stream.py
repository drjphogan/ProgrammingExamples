from struct import pack, unpack, calcsize
from socket import SHUT_WR
from func_tools.factory import Factory


def read_persistable_name(in_stream):
    name = in_stream.restore_string()
    return name


def read_persistable(in_stream):
    persistable_type = read_persistable_name(in_stream)
    persistable = Factory().make(persistable_type)()
    persistable.restore_contents_from(in_stream)
    return persistable


def write_persistable_name(persistable_name, out_stream):
    out_stream.save_string(persistable_name)


def write_persistable(persistable, out_stream):
    persistable.save_name_on(out_stream)
    persistable.save_contents_on(out_stream)


class BaseStream(bytearray):

    def save_numeric(self, v, t):
        self.extend(pack(t, v))

    def save_string(self, v):
        length = len(v)
        self.extend(pack('i', length))
        self.extend(v.encode())

    def save_numeric_array(self, v, t):
        length = len(v)
        self.extend(pack('i', length))
        for item in v:
            self.save_numeric(item, t)

    def save_string_array(self, v):
        length = len(v)
        self.extend(pack('i', length))
        for item in v:
            self.save_string(item)

    def restore_numeric(self, t):
        b = self[:calcsize(t)]
        # note unpack returns a tuple hence [0]
        v = unpack(t, b)[0]
        del self[0:calcsize(t)]
        return v

    def restore_string(self):
        b = self[:calcsize('i')]
        # note unpack returns a tuple hence [0]
        length = unpack('i', b)[0]
        del self[0:calcsize('i')]
        byte_string = self[:length]
        string = byte_string.decode()
        del self[0:length]
        return string

    def restore_numeric_array(self, t):
        length_bytes = self[:calcsize('i')]
        # note unpack returns a tuple hence [0]
        length = unpack('i', length_bytes)[0]
        del self[0:calcsize('i')]
        v = []
        for item in range(length):
            v.append(self.restore_numeric(t))
        return v

    def restore_string_array(self):
        length_bytes = self[:calcsize('i')]
        # note unpack returns a tuple hence [0]
        length = unpack('i', length_bytes)[0]
        del self[0:calcsize('i')]
        v = []
        for item in range(length):
            v.append(self.restore_string())
        return v


class PythonOnlyStream(BaseStream):

    def send(self, conn):
        # send size of byte string
        size = int(len(self))
        conn.send(pack('i', size))
        # send contents of byte string
        conn.send(self)

    def recv(self, conn):
        # get size of byte string - note unpack returns a tuple hence [0]
        size = unpack('i', conn.recv(calcsize('i')))[0]
        # get contents of byte string
        byte_array = conn.recv(size)
        self.extend(byte_array)


class TTCompatibleStream(BaseStream):

    def send(self, conn):
        # send contents of byte string
        conn.send(self)
        conn.shutdown(SHUT_WR)

    def recv(self, conn):
        # read from socket in chunks of 1kb
        chunk_size = 1024
        while True:
            chunk = conn.recv(chunk_size)
            if not chunk:
                break
            else:
                self.extend(chunk)
