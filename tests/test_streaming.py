from scrapy import Request
from scrapy.http import Response
from twisted.internet import reactor

from tests import mock

from scrapy.crawler import Crawler
from testfixtures import LogCapture

from scrapy_streaming.streaming import Streaming
from twisted.trial import unittest

from scrapy_streaming.communication import LogMessage, SpiderMessage, MessageError, CloseMessage, RequestMessage


class FakeProtocol(object):

    def writeLine(self, data):
        pass


class StreamingTest(unittest.TestCase):

    def setUp(self):
        self.streaming = Streaming(FakeProtocol())

    def create_spider(self, name='sample'):
        spider = SpiderMessage.from_dict({'name': name, 'start_urls': []})
        self.streaming.on_message(spider)

    def test_log_message(self):
        log = LogMessage.from_dict({'message': 'test message', 'level': 'debug'})
        with LogCapture() as l:
            self.streaming.on_message(log)

        l.check(('Streaming', 'DEBUG', 'test message'))

    def test_spider_message(self):
        with LogCapture('Streaming') as l:
            self.create_spider()
        l.check(('Streaming', 'DEBUG', 'Spider started: sample'))

        self.assertIsInstance(self.streaming.crawler, Crawler)
        self.assertRaisesRegexp(MessageError, 'Spider already initialized', self.create_spider)

    def test_close_message(self):
        close = CloseMessage.from_dict({})

        self.assertRaisesRegexp(MessageError, 'You must start your spider before sending this message', self.streaming.on_message, close)
        self.create_spider()
        with LogCapture('Streaming') as l:
            self.streaming.on_message(close)
        l.check(('Streaming', 'DEBUG', 'Spider closed'))

    def test_request_message(self):
        request = RequestMessage.from_dict({'id': 'id', 'url': 'http://example.com'})

        self.assertRaisesRegexp(MessageError, 'You must start your spider before sending this message', self.streaming.on_message, request)
        self.create_spider()
        with mock.patch.object(self.streaming.crawler.engine, 'crawl', return_value=None) as mock_method:
            self.streaming.on_message(request)

        self.assertTrue(mock_method.called)

    def test_response_message(self):
        req = Request('http://example.com')
        req.meta['request_id'] = 'test'
        response = Response(url='http://example.com', request=req)

        with mock.patch.object(self.streaming.protocol, 'writeLine') as mock_method:
            self.streaming.send_response(response)

        self.assertTrue(mock_method.called)
