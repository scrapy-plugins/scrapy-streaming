import logging

import six

from scrapy_streaming.utils import MessageError
from scrapy_streaming.utils.fields import EmptyField, RequiredField


class MessageValidator(object):
    """
    This class is responsible for validating dicts keys and values.
    """

    validator = {}
    """
    Validators must be defined as:
        key: name of the field
        value: expected type
    All possible message fields must be defined in the validator.
    """

    def __init__(self, default, fields):
        self.data = fields
        self.validate(fields)
        self.update(default, fields)

    @classmethod
    def from_dict(cls, data, line=None):
        c = cls(data)
        c.line = line
        return c

    def validate(self, data):
        """
        This methods check if the dict ``data`` follows the validator scheme.
        If there is a problem in the validation, raises a MessageError.
        """
        validator = self.validator

        for field, value in data.items():
            if field not in validator:
                raise MessageError('Unknown message field: %s' % field)

            if value is not None and not isinstance(value, validator[field]):
                raise MessageError('%s field must be defined as %s, received: %s' %
                                   (field, validator[field].__name__, type(value).__name__))

    def update(self, default, data):
        """
        After being validated, this method can merge the ``data`` object with the default values.
        If a RequiredField was not provided, raises a MessageError.
        """
        default.update(data)
        for item, value in default.items():
            if isinstance(value, RequiredField):
                raise MessageError('Required field: %s' % item)

            if not isinstance(value, EmptyField):
                setattr(self, item, value)


class RequestMessage(MessageValidator):
    validator = {'id': six.string_types, 'url': six.string_types, 'method': six.string_types,
                 'meta': dict, 'body': six.string_types, 'headers': dict,
                 'cookies': (dict, list), 'encoding': six.string_types,
                 'priority': int, 'dont_filter': bool, 'base64': bool}

    def __init__(self, fields):
        default = {'id': RequiredField(), 'url': RequiredField(), 'method': EmptyField(),
                   'meta': EmptyField(), 'body': EmptyField(), 'headers': EmptyField(),
                   'cookies': EmptyField(), 'encoding': EmptyField(), 'priority': EmptyField(),
                   'dont_filter': EmptyField(), 'base64': False}

        super(RequestMessage, self).__init__(default, fields)
        self.data.pop('base64', None)


class Form(MessageValidator):
    validator = {'formname': six.string_types, 'formxpath': six.string_types,
                 'formcss': six.string_types, 'formnumber': six.string_types,
                 'formdata': dict, 'clickdata': dict, 'dont_click': bool,
                 # request fields
                 'method': six.string_types, 'meta': dict, 'body': six.string_types,
                 'headers': dict, 'cookies': (dict, list), 'encoding': six.string_types,
                 'priority': int, 'dont_filter': bool}

    def __init__(self, form):
        default = {'formname': EmptyField(), 'formxpath': EmptyField(),
                   'formcss': EmptyField(), 'formnumber': EmptyField(),
                   'formdata': EmptyField(), 'clickdata': EmptyField(),
                   'dont_click': EmptyField(),
                   # request fields
                   'method': EmptyField(), 'meta': EmptyField(), 'body': EmptyField(),
                   'headers': EmptyField(), 'cookies': EmptyField(), 'encoding': EmptyField(),
                   'priority': EmptyField(), 'dont_filter': EmptyField()}

        super(Form, self).__init__(default, form)


class FromResponseRequestMessage(RequestMessage):

    def __init__(self, fields):
        if 'from_response_request' not in fields:
            raise MessageError('Required field: from_response_request')
        from_response_request = fields.pop('from_response_request')

        super(FromResponseRequestMessage, self).__init__(fields)
        self.from_response_request = Form.from_dict(from_response_request)


class SpiderMessage(MessageValidator):
    validator = {'name': six.string_types, 'start_urls': list,
                 'allowed_domains': list, 'custom_settings': dict}

    def __init__(self, fields):
        default = {'name': RequiredField(), 'start_urls': RequiredField(),
                   'allowed_domains': EmptyField(), 'custom_settings': EmptyField()}

        super(SpiderMessage, self).__init__(default, fields)


class LogMessage(MessageValidator):
    validator = {'message': six.string_types, 'level': six.string_types}

    def __init__(self, fields):
        default = {'message': RequiredField(), 'level': RequiredField()}

        super(LogMessage, self).__init__(default, fields)
        levels = {'CRITICAL': logging.CRITICAL, 'ERROR': logging.ERROR,
                  'WARNING': logging.WARNING, 'INFO': logging.INFO,
                  'DEBUG': logging.DEBUG}

        if self.level.upper() not in levels:
            raise MessageError('Invalid log level: %s' % self.level)

        self.level = levels[self.level.upper()]


class CloseMessage(MessageValidator):

    def __init__(self, fields):
        super(CloseMessage, self).__init__({}, fields)
