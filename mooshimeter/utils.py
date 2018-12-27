import struct

class UnderflowException(Exception):
    pass

class BytePack:
    """
    Helper class to pack and unpack integers and floats from a buffer
    """
    def __init__(self,bytebuf=[]):
        self.i = 0
        self.bytes = bytebuf[:]
    def putByte(self,v):
        self.bytes.append(v)
    def put(self,v,b=1):
        if type(v) == float:
            v = struct.unpack("BBBB",struct.pack("f",v))
            for e in v:
                self.putByte(e)
        elif type(v) == int:
            while b:
                self.putByte(v&0xFF)
                v >>= 8
                b -= 1
        else:
            # Is it iterable?  Try it, assuming it's a list of bytes
            for byte in v:
                self.putByte(byte)
    def get(self,b=1,t=int,signed=False):
        if t == int:
            if b > self.getBytesRemaining():
                raise UnderflowException()
            r = 0
            s = 0
            top_b = 0
            while b:
                top_b = self.bytes[self.i]
                r += top_b << s
                s += 8
                self.i += 1
                b -= 1
            # Sign extend
            if signed and top_b & 0x80:
                    r -= 1 << s
            return r
        elif t==float:
            if 4 > self.getBytesRemaining():
                raise UnderflowException()
            r = struct.unpack("f",struct.pack("BBBB",*self.bytes[self.i:self.i+4]))
            self.i += 4
            return r[0]
    def getBytes(self, max_bytes=0):
        if max_bytes == 0:
            rval = self.bytes[self.i:]
        else:
            rval = self.bytes[self.i:self.i+max_bytes]
        self.i += len(rval)
        return rval
    def getBytesRemaining(self):
        return len(self.bytes) - self.i


def writeHeader(file, array_name, payload):
    decl_line = "const unsigned char %s[%d]" % (array_name, len(payload))

    # Write header file
    file.write('#define %s_LEN %d\n' % (array_name.upper(), len(payload)))
    file.write('extern ' + decl_line + ';\n')


def writeAsCArray(file, array_name, payload):
    decl_line = "const unsigned char %s[%d]" % (array_name, len(payload))
    # Open main output file
    # Write the opening lines
    file.write(decl_line + '={\n')

    c_on_row = 0

    for c in payload:
        file.write("0x%02X,\t" % ord(c))
        c_on_row += 1
        if (c_on_row == 8):
            c_on_row = 0
            file.write("\n")

    file.write("\n};\n")

# Utility class
class UUID:
    def __init__(self, initializer):
        if type(initializer) == type(""):
            #String input
            self.bytes = self.__stringToBytes(initializer)
        elif type(initializer) == type(1):
            # Integer initialized, assume a 2 byte UUID
            self.bytes = ((initializer>>8)&0xFF, (initializer>>0)&0xFF)
        else:
            #Byte array input
            self.bytes = tuple(initializer)
    def __stringToBytes(self, arg):
        arg = arg.upper()
        arg = arg.replace("-","")
        l = [int(arg[i:i+2],16) for i in range(0,len(arg),2)]
        return tuple(l)
    def __bytesToString(self, bytes):
        l = ["%02X"%bytes[i] for i in range(len(bytes))]
        if len(bytes) == 16:
            l = ["%02X"%bytes[i] for i in range(16)]
            l.insert( 4,'-')
            l.insert( 7,'-')
            l.insert(10,'-')
            l.insert(13,'-')
        return ''.join(l)
    def asString(self):
        return self.__bytesToString(self.bytes)
    def __eq__(self, other):
        return self.bytes==other.bytes
    def __hash__(self):
        return self.asString().__hash__()
    def __str__(self):
        return self.asString()
    def __repr__(self):
        return self.asString()