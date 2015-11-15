calls = {}


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
        lines = data.split('\r\n')

        self.fields = {}
        self.fields['Request-Line'] = lines[0]

        line_iter = iter(lines[1:])
        for line in line_iter:
            if len(line) == 0:
                break
            parts = line.split(':', 1)
            self.fields[parts[0]] = parts[1].strip()

        self.fields['Content'] = ''.join('%s\n' % line
                                         for line in line_iter).strip()

    '''
    Check whether this SIPMessage matches the filter.
    Right now filter is a simple string,
    this should be replaced by something more elaborate later.
    '''
    def matches(self, match):
        return 'SIP' in match

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
        calls[self.fields['Call-ID']] = self


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
