from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

from scrapy_streaming.external_spiderloader import ExternalSpider, ExternalSpiderLoader


class StreamingCommand(ScrapyCommand):
    """
    Command to start stand-alone executables with the the scrapy scrapy_streaming
    """

    requires_project = False

    def syntax(self):
        return "[options] <path of executable>"

    def short_desc(self):
        return "Run a external spider using Scrapy Streaming given its path (doesn't require a project)"

    def add_options(self, parser):
        super(StreamingCommand, self).add_options(parser)

        parser.add_option('-a', '--args', default=[], action='append', metavar="'ARG1,ARG2,...'",
                          help='set command arguments')

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()
        command = args[0]

        arguments = _parse_arguments(opts.args)
        spider = ExternalSpider('StreamingSpider', command, arguments)
        loader = ExternalSpiderLoader.from_settings(self.settings, load_spiders=False)

        loader.crawl(spider)


def _parse_arguments(list_of_args):
    """
    Receives a list with string arguments and split the string arguments by comma
    """
    args = []
    for arg in list_of_args:
        args += [argument.strip() for argument in arg.split(',')]

    return args
