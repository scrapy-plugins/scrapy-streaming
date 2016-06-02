import os

from scrapy import Request
from scrapy.http import Response
from scrapy_streaming.streaming import Streaming
from twisted.internet.defer import Deferred

from scrapy_streaming.utils.spiders import StreamingSpider

from tests.test_commands import ProjectTest
from tests import mock

from scrapy_streaming.utils import get_project_root, dict_serialize, extract_instance_fields


class UtilsTest(ProjectTest):

    def test_get_project(self):
        self.assertEqual(get_project_root(), self.cwd)

    def test_get_project_default(self):
        os.chdir('../')
        self.assertRaises(Exception, get_project_root)

    def test_dict_serialize(self):
        d = {'a': 'b'}
        self.assertEqual(dict_serialize(d), b'{"a": "b"}')

    def test_extract_instance_fields(self):
        class Test(object):
            a = 'a'
            b = 2
            c = {'a': 'b'}
            d = [1, 2, 3]
            e = 2.5
            f = None

        fields = ['a', 'b', 'c', 'd', 'e', 'f']
        expected = {
            'a': 'a',
            'b': 2,
            'c': {'a': 'b'},
            'd': [1, 2, 3],
            'e': 2.5,
            'f': None
        }
        self.assertDictEqual(extract_instance_fields(Test(), fields), expected)

    def test_streaming_spider_parse(self):
        class FakeStreaming(object):
            def send_response(self, resp):
                pass

        spider = StreamingSpider(streaming=FakeStreaming(), name='sample', start_urls=[])

        req = Request('http://example.com')
        req.meta['request_id'] = 'test'
        fake_response = Response('http://example.com', request=req)

        with mock.patch.object(spider.streaming, 'send_response') as mock_send:
            self.assertIsInstance(spider.parse(fake_response), Deferred)

        self.assertTrue(mock_send.called)

    def test_streaming_spider_close(self):
        class FakeStreaming(object):
            def send_response(self, resp):
                pass

        spider = StreamingSpider(streaming=FakeStreaming(), name='sample', start_urls=[])
        spider.close_spider()
        self.assertTrue(spider.stream.called)
