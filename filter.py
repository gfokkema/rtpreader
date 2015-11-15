class Filter:
    def __init__(self):
        self.frame = FrameFilter()
        self.packet = PacketFilter()
        self.datagram = DatagramFilter()


class SubFilter:
    def matches(self):
        return True


class FrameFilter(SubFilter):
    pass


class PacketFilter(SubFilter):
    pass


class DatagramFilter(SubFilter):
    pass
