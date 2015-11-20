from datagram import Datagram
from socket import inet_ntoa

import struct


class Packet:
    @classmethod
    def create(cls, data):
        packet = IPPacket(data)
        return packet
    
    def __repr__(self):
        raise NotImplementedError()


class IPPacket(Packet):
    def __init__(self, data):
        self.version = ord(data[0]) >> 4
        self.header_len = (ord(data[0]) & 0x0f) << 2
        self.size = struct.unpack('>H', data[2:4])[0]
        self.flags = ord(data[6]) >> 5
        self.proto = ord(data[9])
        self.src = inet_ntoa(data[12:16])
        self.dst = inet_ntoa(data[16:20])
        self.datagram = Datagram.create(self.proto, data[self.header_len:])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[%s -> %s size: %d data: %s]" % \
            (self.src, self.dst, self.size, self.datagram)
