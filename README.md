# Scrapy Streaming (WIP)

[![Build Status](https://travis-ci.org/scrapy-plugins/scrapy-streaming.svg?branch=master)](https://travis-ci.org/scrapy-plugins/scrapy-streaming)
[![codecov](https://codecov.io/gh/scrapy-plugins/scrapy-streaming/branch/master/graph/badge.svg)](https://codecov.io/gh/scrapy-plugins/scrapy-streaming)

The Scrapy Streaming provides an interface to write spiders using any programming language, using json objects to make requests, parse web contents, get data, and more.

Also, we officially provide helper libraries to develop your spiders using Java, JS, and R.

## Quickstart

You can read a quick tutorial about scrapy-streaming at http://scrapy-streaming.readthedocs.io/en/latest/quickstart.html

## Usage

You can execute an external spider using the ``streaming`` command, as follows:

    scrapy streaming /path/of/executable

and if you need to use extra arguments, add them using the ``-a`` parameter:

    scrapy streaming my_executable -a arg1 -a arg2 -a arg3,arg4

If you want to integrate this spider with a scrapy's project, define it in the ``external.json`` file in the root of the project.
For example, to add a spider developed in java, and a compiled one, the ``external.json`` can be defined as:

    [
      {
        "name": "java_spider",
        "command": "java",
        "args": ["/home/user/MySpider"]
      },
      {
        "name": "compiled_spider",
        "command": "/home/user/my_executable"
      }
    ]

and then you can execute them using the ``crawl`` command. Inside the project directory, run:

    scrapy crawl spider_name

in this example, ``spider_name`` can be ``java_spider``, ``compiled_spider``, or the name of a Scrapy's spider.

## Documentation

Documentation is available online at http://gsoc2016.readthedocs.io and in the docs directory.
(Temp url, this doc is from the development fork)
