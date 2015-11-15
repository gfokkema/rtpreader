from message import Message

import socket
import struct


class Datagram:
    ip_protos = {
        socket.IPPROTO_UDP: lambda p: UDPDatagram(p),
        socket.IPPROTO_TCP: lambda p: TCPDatagram(p),
        socket.IPPROTO_ICMP: lambda p: ICMPDatagram(p),
    }

    @classmethod
    def create(cls, proto, data):
        datagram = cls.ip_protos.get(proto)
        if datagram is None:
            raise NotImplementedError("IP Protocol %d not supported." % proto)
        return datagram(data)

    def __repr__(self):
        raise NotImplementedError()


class ICMPDatagram(Datagram):
    icmp_codes = {
        (0, 0): 'ECHO reply',
        (8, 0): 'ECHO request',
    }

    def __init__(self, data):
        self.icmp_type = ord(data[0])
        self.icmp_code = ord(data[1])

    def __repr__(self):
        return "[%s]" % self.icmp_codes.get((self.icmp_type, self.icmp_code))


class TCPDatagram(Datagram):
    def __init__(self, data):
        self.srcport = struct.unpack('>H', data[0:2])[0]
        self.dstport = struct.unpack('>H', data[2:4])[0]

        header_len = ord(data[12]) >> 4
        self.size = len(data) - header_len
        self.data = Message.create(data[header_len:])

    def __repr__(self):
        return "[TCP srcport: %d dstport: %d size: %d data: %s]" % \
            (self.srcport, self.dstport, self.size, self.data)


class UDPDatagram(Datagram):
    def __init__(self, data):
        self.srcport = struct.unpack('>H', data[0:2])[0]
        self.dstport = struct.unpack('>H', data[2:4])[0]
        self.size = struct.unpack('>H', data[4:6])[0]
        self.data = Message.create(data[8:])

    def __repr__(self):
        return "[UDP srcport: %d dstport: %d size: %d data: %s]" % \
            (self.srcport, self.dstport, self.size, self.data)
