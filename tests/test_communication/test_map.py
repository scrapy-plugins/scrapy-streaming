from twisted.trial import unittest

from scrapy_streaming.communication.map import _extract_fields


class CommunicationMapTest(unittest.TestCase):

    def test_extract_field(self):
        class Test(object):
            a = 'a'
            b = 2
            c = {'a': 'b'}
            d = [1, 2, 3]
            e = 2.5
            f = None

        fields = ['a', 'b', 'c', 'd', 'e', 'f']
        expected = {
            'a': 'a',
            'b': 2,
            'c': {'a': 'b'},
            'd': [1, 2, 3],
            'e': 2.5,
            'f': None
        }
        self.assertDictEqual(_extract_fields(Test(), fields), expected)
