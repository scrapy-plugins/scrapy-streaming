from scrapy import Spider
from scrapy.http import Request
from twisted.internet import defer


class StreamingSpider(Spider):

    def __init__(self, streaming=None, msg=None, **kwargs):
        self.streaming = streaming
        self.msg = msg
        super(StreamingSpider, self).__init__(**kwargs)
        self.stream = defer.Deferred()

    def parse(self, response):
        # sets the default encoding type with a fake request message
        class FakeMessage(object):
            base64 = False
            line = ''
        msg = FakeMessage()

        response.meta['request_id'] = 'parse'
        self.streaming.send_response(msg, response)
        return self.stream

    def close_spider(self):
        self.stream.callback(None)

    def make_requests_from_url(self, url):
        # adds errback to spider initial requests
        return Request(url, callback=self.parse, dont_filter=True,
                       errback=lambda x: self.streaming.send_exception(self.msg, x.getErrorMessage()))

    def start_requests(self):
        # catch exceptions in spider initial urls
        for url in self.start_urls:
            try:
                yield self.make_requests_from_url(url)
            except (ValueError, TypeError) as e:  # errors raised by request creator
                self.streaming.send_exception(self.msg, str(e))
