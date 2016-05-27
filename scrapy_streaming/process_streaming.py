from scrapy_streaming.communication import CommunicationMap
from scrapy_streaming.line_receiver import LineProcessProtocol
from scrapy_streaming.utils import MessageError


class ProcessStreamingProtocol(LineProcessProtocol):
    """
    This class is responsible for the communication channel between scrapy-streaming and the external spider.
    All messages are sent/received by this class
    """

    def connectionMade(self):
        self.writeLine(CommunicationMap.ready())

    def lineReceived(self, line):
        try:
            msg = CommunicationMap.parse(line)
            print(msg)
        except MessageError as e:
            self.sendError(line, str(e))

    def sendError(self, msg, details):
        self.writeLine(CommunicationMap.error(msg, details))

    def errReceived(self, data):
        print('outReceived')
        print(data)
