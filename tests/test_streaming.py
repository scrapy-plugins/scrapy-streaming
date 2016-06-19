from scrapy import Request
from scrapy.http import Response
from twisted.internet import reactor

from tests import mock

from scrapy.crawler import Crawler
from testfixtures import LogCapture

from scrapy_streaming.streaming import Streaming
from twisted.trial import unittest

from scrapy_streaming.communication import LogMessage, SpiderMessage, MessageError, CloseMessage, RequestMessage, \
    FromResponseRequestMessage, CommunicationMap


class FakeProtocol(object):

    def writeLine(self, data):
        pass

    def closeProcess(self):
        pass


class StreamingTest(unittest.TestCase):

    def setUp(self):
        self.streaming = Streaming(FakeProtocol())

    def tearDown(self):
        try:
            # try to clean the reactor, if necessary
            self.streaming._on_close(None)
        except:
            pass

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

    def test_request_message_missing_url_scheme(self):
        request = RequestMessage.from_dict({'id': 'id', 'url': 'example.com'})

        self.assertRaisesRegexp(MessageError, 'You must start your spider before sending this message', self.streaming.on_message, request)
        self.create_spider()
        with mock.patch.object(self.streaming, 'send_exception', return_value=None) as mock_method:
            self.streaming.on_message(request)

        self.assertTrue(mock_method.called)

    def test_from_response_equest_message(self):
        msg_request = FromResponseRequestMessage.from_dict({'id': 'id', 'url': 'http://example.com', 'from_response_request': {}})
        fake_request = Request('http://example.com', meta={'request_id': 'id'})

        self.assertRaisesRegexp(MessageError, 'You must start your spider before sending this message', self.streaming.on_message, msg_request)
        self.create_spider()
        with mock.patch.object(self.streaming.crawler.engine, 'crawl', return_value=None) as mock_method1:
            self.streaming.on_message(msg_request)

        response = Response(url='http://example.com', request=fake_request)
        response.encoding = 'utf-8'
        response.text = '<form></form>'
        with mock.patch.object(self.streaming.crawler.engine, 'crawl', return_value=None) as mock_method2:
            self.streaming._from_response(msg_request, response)

        self.assertTrue(mock_method1.called)
        self.assertTrue(mock_method2.called)

    def test_from_response_request_missing_form(self):
        msg_request = FromResponseRequestMessage.from_dict({'id': 'id', 'url': 'http://example.com', 'from_response_request': {}})
        fake_request = Request('http://example.com', meta={'request_id': 'id'})

        self.assertRaisesRegexp(MessageError, 'You must start your spider before sending this message', self.streaming.on_message, msg_request)
        self.create_spider()
        with mock.patch.object(self.streaming.crawler.engine, 'crawl', return_value=None) as mock_method1:
            self.streaming.on_message(msg_request)

        response = Response(url='http://example.com', request=fake_request)
        response.encoding = 'utf-8'
        response.text = '<html><body><h1>Test</h1></body></html>'
        with mock.patch.object(self.streaming, 'send_exception', return_value=None) as mock_method2:
            self.streaming._from_response(msg_request, response)

        self.assertTrue(mock_method1.called)
        self.assertTrue(mock_method2.called)

    def test_response_message(self):
        req = Request('http://example.com')
        req.meta['request_id'] = 'test'
        response = Response(url='http://example.com', request=req)
        msg = RequestMessage.from_dict({'id': 'test', 'url': 'http://example.com'})
        with mock.patch.object(self.streaming.protocol, 'writeLine') as mock_method:
            self.streaming.send_response(msg, response)

        self.assertTrue(mock_method.called)

    def test_response_wrong_encoding(self):
        req = Request('http://example.com')
        req.meta['request_id'] = 'test'
        response = Response(url='http://example.com', request=req,
                            body=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x02\x00')
        msg = RequestMessage.from_dict({'id': 'test', 'url': 'http://example.com'})
        with mock.patch.object(self.streaming, 'send_exception') as mock_method:
            self.streaming.send_response(msg, response)

        self.assertTrue(mock_method.called)

    def test_exception_message(self):
        class FakeMessage:
            line = '{"type": "log", "level": "debug", "message": "sample1.py working"}'
        msg = FakeMessage()
        exception = 'Problem in spider'
        with mock.patch.object(self.streaming.protocol, 'writeLine') as mock_method:
            self.streaming.send_exception(msg, exception)

        mock_method.assert_any_call(CommunicationMap.exception(msg.line, exception))
