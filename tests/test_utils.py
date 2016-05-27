import os

from tests.test_commands import ProjectTest


from scrapy_streaming.utils import get_project_root, dict_serialize


class UtilsTest(ProjectTest):

    def test_get_project(self):
        self.assertEqual(get_project_root(), self.cwd)

    def test_get_project_default(self):
        os.chdir('../')
        self.assertRaises(Exception, get_project_root)

    def test_dict_serialize(self):
        d = {'a': 'b'}
        self.assertEqual(dict_serialize(d), b'{"a": "b"}')
