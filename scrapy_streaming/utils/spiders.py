from scrapy import Spider
from twisted.internet import defer


class StreamingSpider(Spider):

    def __init__(self, streaming=None, **kwargs):
        self.streaming = streaming
        super(StreamingSpider, self).__init__(**kwargs)
        self.stream = defer.Deferred()

    def parse(self, response):
        response.meta['request_id'] = 'parse'
        self.streaming.send_response(response)
        return self.stream

    def close_spider(self):
        self.stream.callback(None)
