calls = {}
ports = {}


class SIPMessage(object):
    '''Holds a SIP message, such as:
    * SIPInvite
    * SIPBye

    Fields:
    * request_line
    * call_id
    * reason
    '''

    sip_messages = {
        'INVITE': lambda p: SIPInvite(p),
        'BYE': lambda p: SIPBye(p),
        'SIP/2.0': lambda p: SIPMessage(p),
        'ACK': lambda p: SIPMessage(p),
    }

    '''
    Create a SIP message from some given data.
    '''
    @classmethod
    def create(cls, data):
        sip_message = cls.sip_messages.get(data.split(' ', 1)[0])
        if sip_message is None:
            return None
        return sip_message(data)

    '''
    Create a basic SIP message.
    '''
    def __init__(self, data):
        lines = data.strip().split('\r\n')

        self.fields = {}
        self.fields['Request-Line'] = lines[0]

        line_iter = iter(lines[1:])
        for line in line_iter:
            if len(line) == 0:
                break
            parts = line.split(':', 1)
            self.fields[parts[0]] = parts[1].strip()

        if 'Content-Type' in self.fields and \
                self.fields['Content-Type'] == 'application/sdp':
            line_iter.next()
            self.content = SDPHeader(line_iter)

    def callid(self):
        return self.fields['Call-ID']

    def __repr__(self):
        return '\n' + '\n'.join('  %s: %s' % (f, v)
                                for f, v in self.fields.iteritems())


class SIPInvite(SIPMessage):
    '''
    Holds a SIP INVITE from some given call.

    Fields:
    * request_line
    * call_id
    * reason
    '''
    def __init__(self, data):
        super(SIPInvite, self).__init__(data)
        calls[self.callid()] = self
        ports[self.content.conninfo()] = self

    def __repr__(self):
        return super(SIPInvite, self).__repr__() + '\n' + str(self.content)


class SIPBye(SIPMessage):
    '''
    Holds a SIP BYE from some given call.

    Fields:
    * request_line
    * call_id
    * reason
    '''
    def __init__(self, data):
        super(SIPBye, self).__init__(data)


class SDPHeader:
    '''
    Holds an SDP header containing rtp stream information.
    '''

    def __init__(self, data):
        self.fields = {}
        for line in data:
            parts = line.split('=', 1)
            self.fields.setdefault(parts[0], []).append(parts[1])

    def conninfo(self):
        ip = self.fields['c'][0].split(' ')[2]
        port = self.fields['m'][0].split(' ')[1]
        return ip, port

    def __repr__(self):
        return ''.join('%s %s\r\n' % (k, v)
                       for k, v in self.fields.iteritems())
