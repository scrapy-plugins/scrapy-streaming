import six
from twisted.trial import unittest

from scrapy_streaming.communication import MessageValidator, RequestMessage, SpiderMessage, LogMessage, CloseMessage
from scrapy_streaming.utils import MessageError
from scrapy_streaming.utils.fields import RequiredField, EmptyField


class MessageValidatorTest(unittest.TestCase):

    def test_validate(self):
        class SimpleValidator(MessageValidator):
            validator = {'a': int, 'b': six.string_types, 'c': dict, 'd': (int, float)}

            def __init__(self, data):
                default = {}
                super(SimpleValidator, self).__init__(default, data)

        self.assertRaisesRegexp(MessageError, 'Unknown message field: x', SimpleValidator.from_dict, {'x': 2})
        self.assertRaisesRegexp(MessageError, 'a field must be defined as', SimpleValidator.from_dict, {'a': 'value'})

    def test_required_field(self):
        class SimpleValidator(MessageValidator):
            validator = {'a': int, 'b': six.string_types}

            def __init__(self, data):
                default = {'a': RequiredField(), 'b': None}
                super(SimpleValidator, self).__init__(default, data)

        self.assertRaisesRegexp(MessageError, 'Required field: a', SimpleValidator.from_dict, {})

    def set_attributes(self):
        class SimpleValidator(MessageValidator):
            validator = {'a': int, 'b': list, 'c': int}

            def __init__(self, data):
                default = {'a': RequiredField(), 'b': RequiredField(), 'c': None}
                super(SimpleValidator, self).__init__(default, data)
        a = 3
        b = [1, 2, 3]
        v = SimpleValidator.from_dict({'a': a, 'b': b})

        self.assertEqual(v.a, a)
        self.assertEqual(v.b, b)
        self.assertEqual(v.c, None)

    def test_empty_field(self):
        class SimpleValidator(MessageValidator):
            validator = {'a': int, 'b': list}

            def __init__(self, data):
                default = {'a': None, 'b': EmptyField()}
                super(SimpleValidator, self).__init__(default, data)

        v = SimpleValidator.from_dict({})

        self.assertEqual(v.a, None)
        self.assertEqual(hasattr(v, 'b'), False)


class MessagesTest(unittest.TestCase):

    def test_create_messages(self):
        RequestMessage({'id': u'id', 'url': u'http://example.com'})
        SpiderMessage({'name': u'name', 'start_urls': []})
        LogMessage({'message': u'message', 'level': u'debug'})
        CloseMessage({})
