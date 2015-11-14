from datetime import datetime
from socket import inet_ntoa

import getopt
import pcap
import socket
import struct
import sys


class Packet:
    def __init__(self, packet):
        ip_protos = {
            socket.IPPROTO_UDP: ('UDP', lambda p: self.parse_udp(p)),
            socket.IPPROTO_TCP: ('TCP', lambda p: self.parse_tcp(p)),
        }

        self.version = ord(packet[0]) >> 4
        self.header_len = (ord(packet[0]) & 0x0f) << 2
        self.flags = ord(packet[6]) >> 5
        self.proto = ip_protos.get(ord(packet[9]))
        self.src = inet_ntoa(packet[12:16])
        self.dst = inet_ntoa(packet[16:20])

        if self.proto is None:
            raise NotImplementedError("IP Protocol not supported.")
        self.payload = self.proto[1](packet[self.header_len:])

    def parse_udp(self, payload):
        self.srcport = struct.unpack('>H', payload[0:2])[0]
        self.dstport = struct.unpack('>H', payload[2:4])[0]
        return payload[8:]

    def parse_tcp(self, payload):
        self.srcport = struct.unpack('>H', payload[0:2])[0]
        self.dstport = struct.unpack('>H', payload[2:4])[0]
        return payload[8:]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "proto %s: %s:%d -> %s:%d [size: %d]" % \
            (self.proto[0],
             self.src, self.srcport,
             self.dst, self.dstport,
             len(self.payload))


class RTPReader:
    def __init__(self, pcapfile):
        self.pcap = pcap.pcap(pcapfile)
        self.linktypes = {
            pcap.DLT_RAW: lambda p: p[0:],
            pcap.DLT_EN10MB: lambda p: p[12:],
            pcap.DLT_LINUX_SLL: lambda p: p[14:],
        }
        self.frametypes = {
            '\x08\x00': lambda p: p[2:],                       # IPv4
            '\x81\x00': lambda p: self.frametypes.get(p[4:]),  # 802.1Q
        }

    def parse_link(self, data):
        parse = self.linktypes.get(self.pcap.datalink())
        if parse is None:
            raise NotImplementedError("Unsupported datalink type.")
        return parse(data)

    def parse_frame(self, payload):
        parse = self.frametypes.get(payload[:2])
        if parse is None:
            raise NotImplementedError("Unsupported frame type.")
        return Packet(parse(payload))

    def parse(self):
        for (ts, data) in self.pcap:
            try:
                frame = self.parse_link(data)
                packet = self.parse_frame(frame)
            except NotImplementedError as err:
                print(str(err))
                continue

            time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(time, packet)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hi:o:",
                                   ["help", "input-file=", "output-file="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    in_pcap = None
    # out_pcap = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input-file"):
            in_pcap = a
        # elif o in ("-o", "--output-file"):
        #     out_pcap = a
        else:
            assert False, "Unhandled option"

    try:
        RTPReader(in_pcap).parse()
    except NotImplementedError as err:
        print(str(err))
        sys.exit(2)


def usage():
    print("Usage: " + sys.argv[0] + " -i <input.pcap> [options]")
    print("Options: -i,--input-file  [file] : specify input pcap")
    print("         -o,--output-file [file] : specify output pcap")
    print("         -h,--help               : print this message")


if __name__ == "__main__":
    main()
