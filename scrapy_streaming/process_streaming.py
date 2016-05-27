from scrapy_streaming.communication import CommunicationMap
from scrapy_streaming.line_receiver import LineProcessProtocol


class ProcessStreamingProtocol(LineProcessProtocol):
    """
    This class is responsible for the communication channel between scrapy-streaming and the external spider.
    All messages are sent/received by this class
    """

    def connectionMade(self):
        print('connectionMade')
        import sys
        print(sys.version)
        self.writeLine(CommunicationMap.ready())

    def lineReceived(self, line):
        print('lineReceived')
        print(line)

    def errReceived(self, data):
        print('outReceived')
        print(data)
