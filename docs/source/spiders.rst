External Spiders
================

We define ``External Spider`` as a spider developed in any programming language.

The external spider must communicate using the system ``stdin`` and ``stdout`` with the Streaming.

Stand-alone spiders
-------------------

You can run standalone external spiders using the ``streaming`` command.

.. command:: streaming

streaming
~~~~~~~~~

* Syntax: ``scrapy streaming [options] <path of executable>``
* Requires project: *no*

and if you need to use extra arguments, add them using the ``-a`` parameter::

    scrapy streaming my_executable -a arg1 -a arg2 -a arg3,arg4

So, to execute a java spider named ``MySpider`` for example, you may use::

    scrapy streaming java -a MySpider


Integrate with Scrapy projects
------------------------------

If you want to integrate external spiders with a scrapy's project, create a file named ``external.json``
in your project root. This file must contain an array of json objects, each object with the ``name`` ,
``command``, and ``args`` attributes.

The ``name`` attribute will be used as documented in the :attr:`Spider.name <scrapy:scrapy.spiders.Spider.name>`.
The ``command`` is the path or name of the executable to run your spider. The ``args`` attribute is
optional, this is an array with extra arguments to the command, if any.

For example, if you want to add spider developed in Java and a binary spider, you can define
the ``external.json`` as follows:

.. code-block:: python

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


You can execute external spiders using the ``crawl`` command.

.. command:: crawl

crawl
~~~~~

* Syntax: ``scrapy crawl <spider_name>``
* Requires project: *yes*

This command starts a spider given its name.

Usage examples::

    scrapy crawl java_spider

