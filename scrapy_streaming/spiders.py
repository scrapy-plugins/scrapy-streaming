from scrapy import Spider
from twisted.internet import defer


class StreamingSpider(Spider):

    def __init__(self, process, **kwargs):
        super(StreamingSpider, self).__init__(**kwargs)
        self.process = process
        self.stream = defer.Deferred()

    def parse(self, response):
        return self.stream
