import base64

import simplejson as json

from scrapy import Request
from scrapy.http import Response
from scrapy.utils.python import to_native_str
from twisted.trial import unittest

from scrapy_streaming.communication import CommunicationMap
from scrapy_streaming.utils import MessageError


class CommunicationMapTest(unittest.TestCase):

    def test_invalid_json(self):
        self.assertRaisesRegexp(MessageError, 'Received message is not a valid json.', CommunicationMap.parse, '{a: 2')

    def test_invalid_object(self):
        self.assertRaisesRegexp(MessageError, 'This message is not a json object.', CommunicationMap.parse, '[1, 2, 3]')

    def test_invalid_type(self):
        self.assertRaisesRegexp(MessageError, 'x is not a valid message type.', CommunicationMap.parse, '{"type": "x"}')

    def test_missing_type(self):
        self.assertRaisesRegexp(MessageError, '"type" field not provided.', CommunicationMap.parse, '{"a": 1}')

    def test_ready(self):
        ready = {'type': 'ready', 'status': 'ready'}
        self.assertDictEqual(ready, json.loads(CommunicationMap.ready()))

    def test_error(self):
        error = {'type': 'error', 'received_message': 'message', 'details': 'error details'}

        self.assertEqual(error, json.loads(CommunicationMap.error('message', 'error details')))

    def test_response(self):
        req = Request('http://example.com')
        req.meta['request_id'] = 'test'
        r = Response('http://example.com', request=req)

        resp = {'type': 'response', 'id': 'test', 'url': 'http://example.com',
                'status': 200, 'headers': {}, 'body': '', 'flags': [], 'meta': {'request_id': 'test'}}

        self.assertDictEqual(resp, json.loads(CommunicationMap.response(r, False)))

    def test_response_binary(self):
        req = Request('http://example.com/file.png')
        req.meta['request_id'] = 'test'

        img = b'the binary image data'
        r = Response('http://example.com/file.png', request=req, body=img)

        resp = {'type': 'response', 'id': 'test', 'url': 'http://example.com/file.png',
                'status': 200, 'headers': {}, 'body': to_native_str(base64.b64encode(img)),
                'flags': [], 'meta': {'request_id': 'test'}}

        self.assertDictEqual(resp, json.loads(CommunicationMap.response(r, True)))

    def test_response_binary_missing_encoding(self):
        req = Request('http://example.com/file.png')
        req.meta['request_id'] = 'test'

        img = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x02\x00'
        r = Response('http://example.com/file.png', request=req, body=img)

        self.assertRaisesRegexp(ValueError, 'Response body is not serializable',
                                CommunicationMap.response, r, False)

    def test_exception(self):
        line = '{"type": "log", "level": "debug", "message": "sample1.py working"}'
        exception = 'Logger not found'

        exc = {'type': 'exception', 'received_message': line, 'exception': exception}

        self.assertDictEqual(exc, json.loads(CommunicationMap.exception(line, exception)))
