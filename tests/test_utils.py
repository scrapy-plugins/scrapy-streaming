import os

from tests.test_commands import ProjectTest


from scrapy_streaming.utils import get_project_root, dict_serialize, extract_instance_fields


class UtilsTest(ProjectTest):

    def test_get_project(self):
        self.assertEqual(get_project_root(), self.cwd)

    def test_get_project_default(self):
        os.chdir('../')
        self.assertRaises(Exception, get_project_root)

    def test_dict_serialize(self):
        d = {'a': 'b'}
        self.assertEqual(dict_serialize(d), b'{"a": "b"}')

    def test_extract_instance_fields(self):
        class Test(object):
            a = 'a'
            b = 2
            c = {'a': 'b'}
            d = [1, 2, 3]
            e = 2.5
            f = None

        fields = ['a', 'b', 'c', 'd', 'e', 'f']
        expected = {
            'a': 'a',
            'b': 2,
            'c': {'a': 'b'},
            'd': [1, 2, 3],
            'e': 2.5,
            'f': None
        }
        self.assertDictEqual(extract_instance_fields(Test(), fields), expected)
