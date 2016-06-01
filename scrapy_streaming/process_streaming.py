from twisted.internet import reactor

from scrapy_streaming.communication import CommunicationMap, LogMessage, SpiderMessage
from scrapy_streaming.line_receiver import LineProcessProtocol
from scrapy_streaming.utils import MessageError


class ProcessStreamingProtocol(LineProcessProtocol):
    """
    This class is responsible for the communication channel between scrapy-streaming and the external spider.
    All messages are sent/received by this class
    """

    def __init__(self):
        super(ProcessStreamingProtocol, self).__init__()
        self.spider = None
        self.streaming = ProcessStreaming(self)

    def connectionMade(self):
        self.writeLine(CommunicationMap.ready())

    def lineReceived(self, line):
        try:
            msg = CommunicationMap.parse(line)
            self.streaming.on_message(msg)
        except MessageError as e:
            self.sendError(line, str(e))

    def sendError(self, msg, details):
        self.writeLine(CommunicationMap.error(msg, details))

    def errReceived(self, data):
        print(data)

    def processEnded(self, reason):
        reactor.stop()
        # FIXME add a valid process listener


class ProcessStreaming(object):

    def __init__(self, protocol):
        self.protocol = protocol
        self.mapping = {
            LogMessage: self.on_log,
            SpiderMessage: self.on_spider
        }

    def on_message(self, msg):
        self.mapping[type(msg)](msg)

    def on_log(self, msg):
        import logging
        logging.info(msg.message)
        # FIXME add a real logger

    def on_spider(self, msg):
        pass
