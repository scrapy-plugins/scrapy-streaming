import json
import os

from scrapy_streaming.utils import get_project_root


class ExternalSpider(object):
    """
    Object to represent external spiders defined in ``external.json``.
    """

    def __init__(self, name, command, args=None):
        if args is not None and not isinstance(args, list):
            raise ValueError("'args' must be defined as an array of strings")
        self.name = name
        self.command = command
        self.args = args

    @classmethod
    def from_dict(cls, spider):
        return cls(**spider)


class ExternalSpiderLoader(object):
    """
    This class manages external spiders defined in the ``external.json``
    """

    def __init__(self, settings):
        path = settings.get('EXTERNAL_SPIDERS_PATH', get_project_root())
        # TODO add EXTERNAL_SPIDERS_PATH in docs
        path = os.path.abspath(path)
        self.external = os.path.join(path, 'external.json')
        self._spiders = {}
        self._fetch_spiders()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def _fetch_spiders(self):
        """
        Loads the content in the ``external.json`` file and generate a mapping of external spiders.
        Keep the original mapping if the file is not found.
        Throws JSONDecodeError if it's not a valid json file.
        """
        for spider in _read_json(self.external):
            if not isinstance(spider, dict):
                raise ValueError('External spiders must be defined as json objects.'
                                 ' Read the docs for more information')

            external_spider = ExternalSpider.from_dict(spider)
            self._spiders[external_spider.name] = external_spider
        return self._spiders

    def list(self):
        """
        Returns a list with instance of loaded spiders (ExternalSpider objects)
        """
        return list(self._spiders.values())


def _read_json(path):
    """
    Parse the json given its path. Raises an exception if the file doesn't exist.
    """
    if os.path.isfile(path):
        return json.loads(open(path).read())
    else:
        raise Exception('Could not found "%s" file. Please, check if it\'s in your project root '
                        'or defined in path defined at EXTERNAL_SPIDERS_PATH setting.' % path)
