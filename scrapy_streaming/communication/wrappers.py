import six

from scrapy_streaming.utils import MessageError, RequiredField


class ExternalSpiderMessageWrapper(object):
    validator = {}

    def __init__(self, default, fields):
        self.validate(fields)
        self.update(default, fields)

    @classmethod
    def from_dict(cls, data):
        return cls(data)

    def validate(self, data):
        validator = self.validator
        for key, value in data.items():
            if key not in validator:
                raise MessageError('Unknown message field: %s' % key)

            if value is not None and not isinstance(value, validator[key]):
                raise MessageError('%s field must be defined as %s, received: %s' %
                                   (key, validator[key].__name__, type(value).__name__))

    def update(self, default, data):
        default.update(data)
        for item, value in default.items():
            if isinstance(value, RequiredField):
                raise MessageError('Required field: %s' % item)
            setattr(self, item, value)


class RequestMessage(ExternalSpiderMessageWrapper):
    validator = {'id': six.text_type, 'url': six.text_type}

    def __init__(self, fields):
        default = {'id': None, 'start_urls': None, 'method': None, 'meta': None,
                   'body': None, 'headers': None, 'cookies': None, 'encoding': None,
                   'priority': None, 'dont_filter': None}

        super(RequestMessage, self).__init__(default, fields)


class SpiderMessage(ExternalSpiderMessageWrapper):
    validator = {'name': six.text_type, 'start_urls': list,
                 'allowed_domains': list, 'custom_settings': dict}

    def __init__(self, fields):
        default = {'name': RequiredField(), 'start_urls': RequiredField(),
                   'allowed_domains': None, 'custom_settings': None}

        super(SpiderMessage, self).__init__(default, fields)


class LogMessage(ExternalSpiderMessageWrapper):

    validator = {'message': six.text_type, 'level': six.text_type}

    def __init__(self, fields):
        default = {'message': RequiredField(), 'level': RequiredField()}

        super(LogMessage, self).__init__(default, fields)

    def log(self):
        import logging
        logging.info(self.message)
        # FIXME add a real logger
