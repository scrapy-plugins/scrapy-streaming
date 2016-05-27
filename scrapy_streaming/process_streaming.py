from twisted.internet import reactor

from scrapy_streaming.communication import CommunicationMap, LogMessage
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

            if isinstance(msg, LogMessage):
                msg.log()
        except MessageError as e:
            self.sendError(line, str(e))

    def sendError(self, msg, details):
        self.writeLine(CommunicationMap.error(msg, details))

    def errReceived(self, data):
        print(data)

    def processEnded(self, reason):
        reactor.stop()
        # FIXME add a valid process listener
