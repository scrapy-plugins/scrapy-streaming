import simplejson as json

from scrapy import Request
from scrapy.http import Response
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

        self.assertDictEqual(resp, json.loads(CommunicationMap.response(r)))
