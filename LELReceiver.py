import socket
import struct


class LELReceiver:

    def __init__(self, entity=None, tcp_ip=None, tcp_port=None, num_floats=None):

        print(self)
        if tcp_ip is None:
            tcp_ip = '127.0.0.1'
        if tcp_port is None:
            tcp_port = 19950
        if num_floats is None:
            num_floats = 4

        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.num_floats = num_floats

        print("LELReceiver init for " + self.tcp_ip + ":" + str(self.tcp_port) + ", expecting " + str(self.num_floats) + " floats.")

        self.connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.tcp_ip, self.tcp_port))
        # I think if it errors it won't get to this line?
        self.connected = True
        self.data = list()

    def Receive(self):
        BUFFER_SIZE = 4 * self.num_floats
        if self.connected:
            #print("RECEIVER ON UPDATE")
            buff = ""
            buff = self.s.recv(BUFFER_SIZE)
            #print(buff)
            #print(self.num_floats)
            if not buff:
                self.connected = False
            #import struct
            #self.
            try:
                self.data = struct.unpack('f' * self.num_floats, buff)
            except Exception:
                import sys
                import traceback

                print(globals())
                print(locals())

                traceback.print_tb(sys.exc_info()[2])
            # Acknowledge
            self.s.send('1'.encode('ascii'))

    def getData(self):
        self.Receive()
        return self.data
