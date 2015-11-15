from packet import IPPacket


class Frame:
    frametypes = {
        '\x08\x00': lambda p: EthernetFrame(p),  # IPv4
        '\x81\x00': lambda p: VLANFrame(p),      # 802.1Q
    }

    @classmethod
    def create(cls, data):
        frame = cls.frametypes.get(data[:2])
        if frame is None:
            raise NotImplementedError(
                "Unsupported frame type %s. "
                "See https://en.wikipedia.org/wiki/EtherType." %
                ''.join("\\{:02x}".format(ord(c)) for c in data[:2]))
        return frame(data)

    def matches(self, filter_):
        return filter_.frame.matches() and self.data.matches(filter_)

    def __repr__(self):
        return self.data.__repr__()


class EthernetFrame(Frame):
    def __init__(self, data):
        self.data = IPPacket(data[2:])


class VLANFrame(Frame):
    def __init__(self, data):
        self.data = Frame.create(data[4:])
