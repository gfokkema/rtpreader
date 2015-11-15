from message import Message

import struct


class Datagram:
    pass


class ICMPDatagram(Datagram):
    icmp_codes = {
        (0, 0): 'ECHO reply',
        (8, 0): 'ECHO request',
    }

    def matches(self, match):
        return 'ICMP' in match

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

    def matches(self, match):
        return 'TCP' in match and self.data.matches(match)

    def __repr__(self):
        return "[srcport: %d dstport: %d size: %d data: %s]" % \
            (self.srcport, self.dstport, self.size, self.data)


class UDPDatagram(Datagram):
    def __init__(self, data):
        self.srcport = struct.unpack('>H', data[0:2])[0]
        self.dstport = struct.unpack('>H', data[2:4])[0]
        self.size = struct.unpack('>H', data[4:6])[0]
        self.data = Message.create(data[8:])

    def matches(self, match):
        return 'UDP' in match and self.data.matches(match)

    def __repr__(self):
        return "[srcport: %d dstport: %d size: %d data: %s]" % \
            (self.srcport, self.dstport, self.size, self.data)
