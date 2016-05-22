from scrapy.commands.list import Command

from scrapy_streaming.external_spiderloader import ExternalSpiderLoader


class ListCommand(Command):
    """
    Extends the Scrapy list command, adding external spider to the list
    """

    def run(self, args, opts):
        print('[Scrapy Spiders]')
        super(ListCommand, self).run(args, opts)

        spiders = [spider.name for spider in ExternalSpiderLoader.from_settings(self.settings).list()]
        if spiders:
            print('[External Spiders]')
            for spider in sorted(spiders):
                print(spider)
