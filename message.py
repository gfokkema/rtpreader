from sipmessage import SIPMessage


class Message:
    @classmethod
    def create(cls, data):
        return SIPMessage.create(data)
