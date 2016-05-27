import json

from scrapy.utils.python import to_unicode

from scrapy_streaming.communication import wrappers
from scrapy_streaming.utils import MessageError


class CommunicationMap(object):
    """
    Helper class to create the json messages
    """

    mapping = {
        'spider': wrappers.SpiderMessage,
        'request': wrappers.RequestMessage
    }

    @staticmethod
    def parse(line):
        try:
            msg = json.loads(line)

            if not isinstance(msg, dict):
                raise MessageError('This message is not a json object.')
            if 'type' not in msg:
                raise MessageError('"type" field not provided.')

            msg_type = msg.pop('type')
            try:
                return CommunicationMap.mapping[msg_type].from_dict(msg)
            except KeyError:
                raise MessageError('%s is not a valid message type.' % msg_type)
        except ValueError:
            raise MessageError('Received message is not a valid json.')

    @staticmethod
    def ready():
        fields = {'type': 'ready', 'status': 'ready'}
        return json.dumps(fields)

    @staticmethod
    def error(message, details):
        fields = {'type': 'error',
                  'received_message': to_unicode(message),
                  'details': to_unicode(details)}
        return json.dumps(fields)

    @staticmethod
    def response(resp, request_id='parse'):
        fields = _extract_fields(resp, ['url', 'headers', 'status', 'body', 'meta', 'flags'])
        fields['id'] = to_unicode(request_id)
        return json.dumps(fields)


def _extract_fields(item, fields):
    data = {}
    for field in fields:
        data[field] = json.dumps(getattr(item, field))
    return data
