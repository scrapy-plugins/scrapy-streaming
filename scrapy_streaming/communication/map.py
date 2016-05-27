from scrapy.utils.python import to_bytes

from scrapy_streaming.communication import wrappers


class CommunicationMap(object):
    """
    Helper class to create the json messages
    """

    @staticmethod
    def ready():
        return wrappers.ReadyMessage.parse()

    @staticmethod
    def response(resp, request_id=b'parse'):
        fields = _extract_fields(resp, ['url', 'headers', 'status', 'body', 'meta', 'flags'])
        fields[b'id'] = to_bytes(request_id)

        return wrappers.ResponseMessage.parse(fields)


def _extract_fields(item, fields):
    data = {}
    for field in fields:
        data[to_bytes(field)] = to_bytes(getattr(item, field))

    return data
