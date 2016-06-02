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
    def from_dict(cls, data):
        return cls(data)

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
                 'priority': int, 'dont_filter': bool}

    def __init__(self, fields):
        default = {'id': RequiredField(), 'url': RequiredField(), 'method': EmptyField(),
                   'meta': EmptyField(), 'body': EmptyField(), 'headers': EmptyField(),
                   'cookies': EmptyField(), 'encoding': EmptyField(), 'priority': EmptyField(),
                   'dont_filter': EmptyField()}

        super(RequestMessage, self).__init__(default, fields)


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
