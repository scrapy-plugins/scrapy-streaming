#!/usr/bin/env python
from setuptools import setup

setup(
    name='scrapy-streaming',
    version='0.1',
    url='https://github.com/scrapy-plugins/scrapy-streaming',
    description='Develop Spiders using any Programming Language',
    author='Scrapy developers',
    packages=['streaming'],
    requires=['scrapy'],

    entry_points={
        'scrapy.commands': [
            'streaming=streaming.commands.streaming:StreamingCommand',
            'list=streaming.commands.list:ListCommand',
            'crawl=streaming.commands.crawl:CrawlCommand'
        ],
    },
)
