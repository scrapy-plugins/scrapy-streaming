from scrapy import Request
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from scrapy_streaming.communication import CommunicationMap, LogMessage, SpiderMessage, RequestMessage, CloseMessage
from scrapy_streaming.communication.line_receiver import LineProcessProtocol
from scrapy_streaming.utils import MessageError
from scrapy_streaming.utils.spiders import StreamingSpider


class StreamingProtocol(LineProcessProtocol):
    """
    This class is responsible for the low-level communication channel between scrapy-streaming and the external spider.
    All messages are sent/received by this class.
    """

    def __init__(self):
        super(StreamingProtocol, self).__init__()
        self.streaming = Streaming(self)

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


class Streaming(object):
    """
    This class contains the high-level communication channel between scrapy-streaming and the external spider.
    The logic and workflow is processed here. All received messages and sent pass through this class.

    Incoming messages are in the methods started with on_<meth name>. Outcoming messages are in methods that
    starts with send_<method name>
    """

    def __init__(self, protocol):
        self.protocol = protocol
        self.crawler = None
        self.mapping = {
            LogMessage: self.on_log,
            SpiderMessage: self.on_spider,
            RequestMessage: self.on_request,
            CloseMessage: self.on_close
        }

    def on_message(self, msg):
        self.mapping[type(msg)](msg)

    def on_log(self, msg):
        import logging
        logging.info(msg.message)
        # FIXME add a real logger

    def on_spider(self, msg):
        if self.crawler is not None:
            raise MessageError('Spider already initialized')
        fields = {'streaming': self}
        fields.update(msg.data)

        runner = CrawlerRunner()
        self.crawler = runner.create_crawler(StreamingSpider)
        dfd = runner.crawl(self.crawler, **fields)
        dfd.addBoth(lambda _: reactor.stop())

    def on_request(self, msg):
        # update request with id field
        request_id = msg.data.pop('id')
        meta = msg.data.pop('meta', {})
        meta['request_id'] = request_id
        msg.data['meta'] = meta

        r = Request(callback=self.send_response, **msg.data)
        self.crawler.engine.crawl(r, self.crawler.spider)

    def on_close(self, msg):
        self.crawler.stop()
        self.crawler.spider.close_spider()

    def send_response(self, response):
        self.protocol.writeLine(CommunicationMap.response(response))
