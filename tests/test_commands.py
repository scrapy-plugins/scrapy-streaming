import os
import shutil
import subprocess
import tempfile
from tempfile import mkdtemp

from os.path import join

import sys
from time import sleep

from scrapy.utils.python import to_native_str
from scrapy.utils.test import get_testenv
from shutil import rmtree
from twisted.trial import unittest

from scrapy_streaming.commands.streaming import _parse_arguments


class ProjectTest(unittest.TestCase):
    project_name = 'testproject'

    def setUp(self):
        self.temp_path = mkdtemp()
        self.cwd = self.temp_path
        self.proj_path = join(self.temp_path, self.project_name)
        self.proj_mod_path = join(self.proj_path, self.project_name)
        self.env = get_testenv()

        self.call('startproject', self.project_name)
        self.cwd = join(self.temp_path, self.project_name)
        os.chdir(self.cwd)
        self.env['SCRAPY_SETTINGS_MODULE'] = '%s.settings' % self.project_name
        self.external_path = join(self.cwd, 'external.json')
        with open(self.external_path, 'w') as external:
            external.write('''
[
  {
    "name": "PythonSpider",
    "command": "spiders/sample1.py"
  },

  {
    "name": "JavaSpider",
    "command": "java",
    "args": ["MyClass"]
  }
]
''')

    def tearDown(self):
        rmtree(self.temp_path)

    def call(self, *new_args, **kwargs):
        with tempfile.NamedTemporaryFile() as out:
            args = (sys.executable, '-m', 'scrapy.cmdline') + new_args
            return subprocess.call(args, stdout=out, stderr=out, cwd=self.cwd,
                env=self.env, **kwargs)

    def proc(self, *new_args, **kwargs):
        args = (sys.executable, '-m', 'scrapy.cmdline') + new_args
        p = subprocess.Popen(args, cwd=self.cwd, env=self.env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             **kwargs)

        waited = 0
        interval = 0.2
        while p.poll() is None:
            sleep(interval)
            waited += interval
            if waited > 15:
                p.kill()
                assert False, 'Command took too much time to complete'

        return p


class ListCommandTest(ProjectTest):

    def test_list_is_running(self):
        self.assertEqual(0, self.call('list'))

    def test_external_spiders(self):
        p = self.proc('list')
        out = to_native_str(p.stdout.read())

        self.assertIn("JavaSpider", out)
        self.assertIn("PythonSpider", out)


class StreamingCommandTest(ProjectTest):

    def test_parse_arguments(self):
        args1 = ['a,b,c']
        args2 = ['a,b,c', 'c,d']

        self.assertListEqual(_parse_arguments(args1), ['a', 'b', 'c'])
        self.assertListEqual(_parse_arguments(args2), ['a', 'b', 'c', 'c', 'd'])

    def test_usage_error(self):
        p = self.proc('streaming')
        log = to_native_str(p.stdout.read())

        self.assertIn('Usage', log)

    def test_streaming(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test1 = os.path.join(path, 'spiders', 'sample1.py')
        p = self.proc('streaming', test1)
        log = to_native_str(p.stderr.read())

        self.assertIn('sample1.py working', log)

    def test_streaming_wrong_message(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test1 = os.path.join(path, 'spiders', 'wrong_message.py')
        p = self.proc('streaming', test1)
        log = to_native_str(p.stderr.read())

        self.assertIn('invalid_type is not a valid message type.', log)

    def test_streaming_args(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test1 = os.path.join(path, 'spiders', 'sample1.py')
        p = self.proc('streaming', 'python', '-a', test1)
        log = to_native_str(p.stderr.read())

        self.assertIn('sample1.py working', log)

    def test_streaming_request_exception(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test1 = os.path.join(path, 'spiders', 'request_exception.py')
        p = self.proc('streaming', test1)
        log = to_native_str(p.stderr.read())

        self.assertIn('Scrapy raised an exception', log)

    def test_streaming_external_error(self):
        path = os.path.abspath(os.path.dirname(__file__))
        test1 = os.path.join(path, 'spiders', 'error_spider.py')
        p = self.proc('streaming', test1)
        log = to_native_str(p.stderr.read())

        self.assertIn('Closing the process due to this error', log)


class CrawlCommandTest(ProjectTest):

    def setUp(self):
        super(CrawlCommandTest, self).setUp()
        test_path = os.path.abspath(os.path.dirname(__file__))
        shutil.copytree(os.path.join(test_path, 'spiders'), os.path.join(self.cwd, 'spiders'))

    def test_crawl_invalid_spider(self):
        p = self.proc('crawl', 'unknown_spider')
        log = to_native_str(p.stderr.read())

        self.assertIn("KeyError: 'unknown_spider'", log)

    def test_crawl(self):
        p = self.proc('crawl', 'PythonSpider')
        log = to_native_str(p.stderr.read())

        self.assertIn('sample1.py working', log)
