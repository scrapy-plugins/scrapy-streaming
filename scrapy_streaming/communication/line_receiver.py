from scrapy.utils.python import to_bytes
from twisted.internet import protocol


class LineProcessProtocol(protocol.ProcessProtocol, object):
    """
    This class extends the twisted ProcessProtocol to split the incoming data in lines.
    The data received by ``outReceived`` if added to an internal buffer, and dispatched by ``lineReceived``
    """

    def __init__(self):
        self._buffer = b''
        self._delimiter = b'\n'

    def outReceived(self, data):
        """
        Implement the outReceived method, buffering the incoming data and
        dispatching line by line in the ``lineReceived`` method.
        """
        self._buffer += data

        lines = self._buffer.splitlines()
        if data.endswith(self._delimiter):
            self._buffer = b''
        else:
            self._buffer = lines.pop()

        for line in lines:
            self.lineReceived(line)

    def lineReceived(self, line):
        """
        An entire line received by process stdout. You must implement this method to use this class.
        """
        raise NotImplementedError

    def writeLine(self, data):
        """
        Write the data to the process stdin, adding the new-line delimiter if necessary
        """
        data = to_bytes(data)
        if not data.endswith(b'\n'):
            data += self._delimiter
        self.transport.write(data)
