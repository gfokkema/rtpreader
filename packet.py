from datagram import ICMPDatagram, TCPDatagram, UDPDatagram
from socket import inet_ntoa

import socket
import struct


class IPPacket:
    ip_protos = {
        socket.IPPROTO_UDP: ('UDP', lambda p: UDPDatagram(p)),
        socket.IPPROTO_TCP: ('TCP', lambda p: TCPDatagram(p)),
        socket.IPPROTO_ICMP: ('ICMP', lambda p: ICMPDatagram(p)),
    }

    def __init__(self, data):
        self.version = ord(data[0]) >> 4
        self.header_len = (ord(data[0]) & 0x0f) << 2
        self.size = struct.unpack('>H', data[2:4])[0]
        self.flags = ord(data[6]) >> 5
        self.proto = self.ip_protos.get(ord(data[9]))
        self.src = inet_ntoa(data[12:16])
        self.dst = inet_ntoa(data[16:20])

        if self.proto is None:
            raise NotImplementedError("IP Protocol %d not supported." %
                                      ord(data[9]))
        self.datagram = self.proto[1](data[self.header_len:])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "proto %s: %s -> %s [size: %d] - %s" % \
            (self.proto[0],
             self.src, self.dst,
             self.size,
             self.datagram)
