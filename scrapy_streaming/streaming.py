import logging

from scrapy import Request, FormRequest
from scrapy.crawler import CrawlerRunner
from scrapy.utils.python import to_native_str
from twisted.internet import reactor
from twisted.internet.error import ProcessExitedAlready

from scrapy_streaming.communication import CommunicationMap, LogMessage, SpiderMessage, RequestMessage, CloseMessage, \
    FromResponseRequestMessage
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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.streaming = Streaming(self)
        self._closing = False

    def connectionMade(self):
        self.writeLine(CommunicationMap.ready())

    def lineReceived(self, line):
        try:
            msg = CommunicationMap.parse(line)
            self.streaming.on_message(msg)
        except MessageError as e:
            self.sendError(line, str(e))

    def sendError(self, msg, details):
        self.logger.error('Received message: ' + to_native_str(msg))
        self.logger.error(details)
        self.writeLine(CommunicationMap.error(msg, details))
        self.closeProcess()

    def errReceived(self, data):
        self.logger.error('Received error from external spider')
        self.logger.error(data)
        self.logger.error('Closing the process due to this error')
        self.closeProcess()

    def processEnded(self, status):
        self.logger.debug("Process ended")
        self.closeProcess()

    def closeProcess(self):
        if self._closing:
            return
        self._closing = True
        self.transport.loseConnection()
        try:  # kill the process if it still running
            pid = self.transport.pid
            self.transport.signalProcess('KILL')
            self.logger.debug('Killing the process %s' % pid)
        except ProcessExitedAlready:
            pass
        reactor.stop()


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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.mapping = {
            LogMessage: self._on_log,
            SpiderMessage: self._on_spider,
            RequestMessage: self._on_request,
            FromResponseRequestMessage: self._on_from_response_request,
            CloseMessage: self._on_close
        }

    def on_message(self, msg):
        if not isinstance(msg, LogMessage) and not isinstance(msg, SpiderMessage) and self.crawler is None:
            raise MessageError('You must start your spider before sending this message')
        self.mapping[type(msg)](msg)

    def _on_log(self, msg):
        self.logger.log(msg.level, msg.message)

    def _on_spider(self, msg):
        if self.crawler is not None:
            raise MessageError('Spider already initialized')
        fields = {'streaming': self, 'msg': msg}
        fields.update(msg.data)

        runner = CrawlerRunner()
        self.crawler = runner.create_crawler(StreamingSpider)
        dfd = runner.crawl(self.crawler, **fields)
        dfd.addBoth(lambda x: self.protocol.closeProcess())

        self.logger.debug('Spider started: %s' % msg.name)

    def _on_request(self, msg, callback=None):
        if callback is None:
            callback = self.send_response
        # update request with id field
        request_id = msg.data.pop('id')
        meta = msg.data.pop('meta', {})
        meta['request_id'] = request_id
        msg.data['meta'] = meta

        try:
            r = Request(callback=lambda x: callback(msg, x),
                        errback=lambda x: self.send_exception(msg, x.getErrorMessage()),
                        **msg.data)
            self.crawler.engine.crawl(r, self.crawler.spider)
        except (ValueError, TypeError) as e:  # errors raised by request creator
            self.send_exception(msg, str(e))

    def _on_from_response_request(self, msg):
        self._on_request(msg, self._from_response)

    def _from_response(self, msg, response):
        request_id = response.meta['request_id']

        meta = msg.from_response_request.data.pop('meta', {})
        meta['request_id'] = request_id
        msg.from_response_request.data['meta'] = meta
        try:
            # check for possible problems in the response
            r = FormRequest.from_response(response, callback=lambda x: self.send_response(msg, x),
                                          errback=lambda x: self.send_exception(msg, x.getErrorMessage()),
                                          **msg.from_response_request.data)
            self.crawler.engine.crawl(r, self.crawler.spider)
        except (ValueError, IndexError) as e:  # errors raised by from_response
            self.send_exception(msg, str(e))

    def _on_close(self, msg):
        self.crawler.stop()
        self.crawler.spider.close_spider()
        self.protocol.closeProcess()

        self.logger.debug('Spider closed')

    def send_response(self, msg, response):
        try:
            self.protocol.writeLine(CommunicationMap.response(response, msg.base64))
        except ValueError as e:  # problems in the encoding
            self.send_exception(msg, str(e))

    def send_exception(self, msg, details):
        self.logger.error('Scrapy raised an exception: ' + details)
        self.logger.error('Caused by: ' + to_native_str(msg.line))
        self.protocol.writeLine(CommunicationMap.exception(msg.line, details))
