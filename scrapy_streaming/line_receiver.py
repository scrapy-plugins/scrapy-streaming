from scrapy.utils.python import to_bytes
from twisted.internet import protocol


class LineProcessProtocol(protocol.ProcessProtocol, object):
    """
    This class extends the twisted ProcessProtocol to split the incoming data in lines.
    The data received by ``outReceived`` if added to an internal buffer, and dispatched by ``lineReceived``
    """

    def __init__(self):
        self.__buffer = b''
        self.__delimiter = b'\n'

    def outReceived(self, data):
        """
        Implement the outReceived method, buffering the incoming data and
        dispatching line by line in the ``lineReceived`` method.
        """
        self.__buffer += data

        lines = self.__buffer.splitlines()
        if data.endswith(self.__delimiter):
            self.__buffer = b''
        else:
            self.__buffer = lines.pop()

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
            data += self.__delimiter
        self.transport.write(data)
