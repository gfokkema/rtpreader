from sipmessage import SIPMessage


class Message:
    @classmethod
    def create(cls, data):
        return SIPMessage.create(data) or Message(data)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '[unknown]'
