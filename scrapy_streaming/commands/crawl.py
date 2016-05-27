from scrapy.commands.crawl import Command

from scrapy_streaming.external_spiderloader import ExternalSpiderLoader


class CrawlCommand(Command):
    """
    Extends the scrapy crawl command, adding the possibility to start a external spider using the crawl command
    """

    def run(self, args, opts):
        try:
            super(CrawlCommand, self).run(args, opts)
        except KeyError:
            spname = args[0]

            ExternalSpiderLoader.from_settings(self.settings).crawl(spname)
