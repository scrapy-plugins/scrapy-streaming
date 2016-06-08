import base64

import simplejson as json

from scrapy.utils.python import to_unicode, to_native_str

from scrapy_streaming.communication import validators
from scrapy_streaming.utils import MessageError, extract_instance_fields


class CommunicationMap(object):
    """
    Helper class to create and receive json messages
    """

    mapping = {
        'spider': validators.SpiderMessage,
        'request': validators.RequestMessage,
        'form_request': validators.FormRequestMessage,
        'log': validators.LogMessage,
        'close': validators.CloseMessage
    }

    @staticmethod
    def parse(line):
        """
        Receives a json string in a line, that will be decoded and parsed to a message
        """
        try:
            msg = json.loads(to_native_str(line))

            if not isinstance(msg, dict):
                raise MessageError('This message is not a json object.')
            if 'type' not in msg:
                raise MessageError('"type" field not provided.')

            msg_type = msg.pop('type')
            if msg_type not in CommunicationMap.mapping:
                raise MessageError('%s is not a valid message type.' % msg_type)

            return CommunicationMap.mapping[msg_type].from_dict(msg, line)
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
    def response(resp, encode64):
        fields = extract_instance_fields(resp, ['url', 'headers', 'status', 'meta', 'flags'])
        if encode64:
            fields['body'] = base64.b64encode(resp.body)
        else:
            # validates if the body is text-like and serializable
            try:
                json.dumps(resp.body)  # throws UnicodeDecodeError if not text-serializable
                fields['body'] = resp.body
            except UnicodeDecodeError:
                raise ValueError('Response body is not serializable. If it\'s returning binary data, '
                                 'set the "base64" to True to encode the data.')

        fields['id'] = resp.meta['request_id']
        fields['type'] = 'response'

        return json.dumps(fields)

    @staticmethod
    def exception(line, exception):
        fields = {'type': 'exception',
                  'received_message': to_unicode(line),
                  'exception': to_unicode(exception)}

        return json.dumps(fields)
