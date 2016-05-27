from scrapy_streaming.utils import WrongMessage


class StreamingMessageWrapper(object):
    template = b''

    @classmethod
    def parse(cls, dict_args=None):
        msg = b''.join([line.strip() for line in cls.template.splitlines()])
        if dict_args:
            return msg % dict_args
        return msg


class ExternalSpiderMessageWrapper(object):

    validator = {}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def validate(self):
        for field in self.validator:
            attr = getattr(self, field[0])
            if not isinstance(attr, field[1]):
                raise WrongMessage('%s field must be defined as %s, received: %s' %
                                   (field[0], field[1].__name__, type(attr).__name__))


# Scrapy Streaming Messages
# -------------------------


class ReadyMessage(StreamingMessageWrapper):
    template = b'{"type":"status","status":"ready"}'


class ResponseMessage(StreamingMessageWrapper):
    template = b'''
{
    "type":"response",
    "id":'%(id)s',
    "url":'%(url)s',
    "headers":%(headers)s,
    "status":%(status)s,
    "body":'%(body)s',
    "meta":%(meta)s,
    "flags":%(flags)s
}'''


# External Spider Messages
# ------------------------

class RequestMessage(ExternalSpiderMessageWrapper):

    def __init__(self, id, url, method=None, meta=None, body=None, headers=None,
                       cookies=None, encoding=None, priority=None, dont_filter=None):
        self.id = id
        self.url = url

        self.validate()
