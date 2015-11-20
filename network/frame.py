from network.packet import Packet


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

    def __repr__(self):
        return self.data.__repr__()


class VLANFrame(Frame):
    def __init__(self, data):
        self.data = Frame.create(data[4:])


class EthernetFrame(Frame):
    def __init__(self, data):
        self.data = Packet.create(data[2:])