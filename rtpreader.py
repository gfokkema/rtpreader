from datetime import datetime
from packet import IPPacket

import pcap


class RTPReader:
    '''This class will read and parse a pcap source.'''
    linktypes = {
        pcap.DLT_RAW: lambda p: p[0:],
        pcap.DLT_EN10MB: lambda p: p[12:],
        pcap.DLT_LINUX_SLL: lambda p: p[14:],
    }

    def __init__(self, pcapfile):
        self.frametypes = {
            '\x08\x00': lambda p: p[2:],                       # IPv4
            '\x81\x00': lambda p: self.frametypes.get(p[4:]),  # 802.1Q
        }
        self.pcap = pcap.pcap(pcapfile)

    def parse_link(self, data):
        parse = self.linktypes.get(self.pcap.datalink())
        if parse is None:
            raise NotImplementedError("Unsupported datalink type. %d" %
                                      self.pcap.datalink())
        return parse(data)

    def parse_frame(self, data):
        parse = self.frametypes.get(data[:2])
        if parse is None:
            raise NotImplementedError(
                "Unsupported frame type %s. "
                "See https://en.wikipedia.org/wiki/EtherType." %
                ''.join("\\{:02x}".format(ord(c)) for c in data[:2]))
        return IPPacket(parse(data))

    def parse(self):
        for (ts, data) in self.pcap:
            try:
                frame = self.parse_link(data)
                packet = self.parse_frame(frame)
            except NotImplementedError as err:
                print(str(err))
                continue

            time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            if packet.matches(''):
                print(time, packet)
