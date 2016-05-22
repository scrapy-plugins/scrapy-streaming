from tests.test_commands import ProjectTest
from twisted.trial import unittest

from scrapy_streaming.external_spiderloader import ExternalSpider, ExternalSpiderLoader, _read_json


class ExternalSpiderTest(unittest.TestCase):

    def test_wrong_arg_type(self):
        params = {'name': 'Name', 'command': 'python', 'args': {'a': 'b'}}
        self.assertRaises(ValueError, ExternalSpider.from_dict, params)


class ExternalSpiderLoaderTest(ProjectTest):

    def test_list(self):
        e = ExternalSpiderLoader({})

        self.assertEqual(2, len(e.list()))

    def test_invalid_json(self):
        open(self.external_path, 'w').write('''
[
  {
    "name": "PythonSpider",
    "command": "scripts/dmoz.py"
  },
''')
        self.assertRaises(ValueError, ExternalSpiderLoader.from_settings, {})

    def test_invalid_json_content(self):
        open(self.external_path, 'w').write('''
{
  "name": "PythonSpider",
  "command": "scripts/dmoz.py"
}
''')
        self.assertRaises(ValueError, ExternalSpiderLoader.from_settings, {})

    def test_invalid_file(self):
        self.assertEqual([], _read_json('/fff'))
