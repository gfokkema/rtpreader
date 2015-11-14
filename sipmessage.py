class SIPMessage(object):
    sip_messages = {
        'INVITE': lambda p: SIPInvite(p),
        'BYE': lambda p: SIPBye(p),
        'SIP/2.0': None,
        'ACK': None,
    }

    @classmethod
    def create(cls, data):
        sip_message = cls.sip_messages.get(data.split(' ', 1)[0])
        if sip_message is None:
            return None
        return sip_message(data)

    def __init__(self, data):
        self.fields = data.split('\n', 1)


class SIPInvite(SIPMessage):
    def __init__(self, data):
        super(SIPInvite, self).__init__(data)


class SIPBye(SIPMessage):
    def __init__(self, data):
        super(SIPBye, self).__init__(data)
