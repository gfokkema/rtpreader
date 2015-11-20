from datetime import datetime
from network.frame import Frame

import pcap


class RTPReader:
    '''This class will read and parse a pcap source.'''
    linktypes = {
        pcap.DLT_RAW: lambda p: p[0:],
        pcap.DLT_EN10MB: lambda p: p[12:],
        pcap.DLT_LINUX_SLL: lambda p: p[14:],
    }
    filter_ = 'port 5060'

    def __init__(self, pcapfile):
        self.pcap = pcap.pcap(pcapfile)
        self.pcap.setfilter(self.filter_)
        self.link = self.linktypes.get(self.pcap.datalink())
        if self.link is None:
            raise NotImplementedError("Unsupported datalink type %d." %
                                      self.pcap.datalink())

    def setfilter(self, filter_):
        self.pcap.setfilter(filter_)

    def parse(self):
        for (ts, data) in self.pcap:
            try:
                frame = Frame.create(self.link(data))
            except NotImplementedError as err:
                print(str(err))
                continue

            time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(time, frame)
