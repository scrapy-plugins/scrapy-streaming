from scrapy_streaming.communication.line_receiver import LineProcessProtocol
from twisted.trial import unittest

from tests import mock


class LineReceiverTest(unittest.TestCase):

    def setUp(self):
        self.receiver = LineProcessProtocol()

    def test_buffering(self):

        with mock.patch.object(self.receiver, 'lineReceived') as mock_method:
            self.receiver.outReceived(b'received data \n with multiple \n lines')

        mock_method.assert_any_call(b'received data ')
        mock_method.assert_any_call(b' with multiple ')

        self.assertEqual(self.receiver._buffer, b' lines')

    def test_must_implement_lineReceived(self):
        self.assertRaises(NotImplementedError, self.receiver.outReceived, b'test\n')
