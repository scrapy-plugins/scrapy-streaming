import os

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError


class StreamingCommand(ScrapyCommand):
    """
    Command to start stand-alone executables with the the scrapy scrapy_streaming
    """

    requires_project = False

    def syntax(self):
        return "[options] <path of executable>"

    def short_desc(self):
        return "Run a external spider using Scrapy Streaming given its path (doesn't require a project)"

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()
        filename = args[0]
        if not os.path.exists(filename):
            raise UsageError("File not found: %s\n" % filename)

        raise NotImplementedError()
