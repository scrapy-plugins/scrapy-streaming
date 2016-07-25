.. _node:

Node.js Package
===============

.. currentmodule:: node


.. todo:: publish it and add the link to npm package with the package docs here

We provide a helper library to help the development process of external spiders in JavaScript using Node.js.

It's recommended to read the :ref:`quickstart` before using this package.

Installation
------------

To install the ``scrapystreaming`` package, runs:

.. code-block:: js

    npm install scrapystreaming

and loads it using:

.. code-block:: js

    var scrapy = require('scrapystreaming');


scrapystreaming
---------------


The ``scrapystreaming`` Node package provide the following commands:

* :meth:`createSpider`
* :meth:`closeSpider`
* :meth:`sendLog`
* :meth:`sendRequest`
* :meth:`sendFromResponseRequest`
* :meth:`runSpider`

.. tip:: The Scrapy Streaming and your spider communicates using the system ``stdin``, ``stdout``, and ``stderr``.
         So, don't write any data that is not a json message to the system ``stdout`` or ``stderr``.

         These commands write and read data from ``stdin``, ``stdout``, and ``stderr`` when necessary, so you don't need to handle
         the communication channel manually.

.. method:: create_spider(name, startUrls, callback, [allowedDomains, customSettings])


    :param string name:                 name of the
    :param array startUrls:             list of initial
    :param Function callback:           callback to handle the responses from
    :param array allowedDomains:        list of allowed
    :param object customSettings:       custom settings to be used in Scrapy

    This command is used to create and run a Spider, sending the :message:`spider` message.

Usages:

.. code-block:: js

    var callback = function(response) {
        // handle the response message
    };

    // usage 1, all parameters
    scrapy.createSpider('sample', ['http://example.com'], callback,
                        ['example.com'], {some_setting: 'some value'});
    // usage 2, empty spider

    scrapy.createSpiders("sample", [], parse);


.. method:: closeSpider()

Closes the spider, sending the :message:`close` message.

Usage:

.. code-block:: js

    scrapy.closeSpider();


.. method:: sendLog(message, level)

    :param string message:  log message
    :param string level:    log level, must be one of 'CRITICAL', 'ERROR', 'WARNING', 'INFO', and 'DEBUG'

Send a log message to the Scrapy Streaming's logger output. This commands sends the :message:`log` message.

Usages:

.. code-block:: js

    // logging some error
    sendLog("something wrong", "error")

.. method:: sendRequest(url, callback, config)

    :param string       url:                    request url
    :param function     callback:               response callback
    :param object       config:                 object with extra request parameters (optional)
    :param boolean      config.base64:          if true, converts the response body to base64. (optional)
        :param string       config.method           request method (optional)
    :param object       config.meta:            request extra data (optional)
    :param string       config.body:            request body (optional)
    :param object       config.headers:         request headers (optional)
    :param object       config.cookies:         rqeuest extra cookies (optional)
    :param string       config.encoding:        default encoding (optional)
    :param int          config.priority:        request priority  (optional)
    :param boolean      config.dont_filter:     if true, the request don't pass on the request duplicate filter (optional)

Open a new request, using the :message:`request` message.

Usages:

.. code-block:: js

    var callback = function(response) {
        // parse the response
    };

    scrapy.sendRequest('http://example.com', callback);

    // base64 encoding, used to request binary content, such as files
    var config = {base64: true};
    scrapy.sendRequest('http://example.com/some_file.xyz', callback, config)

.. method:: sendFromResponseRequest(url, callback, fromResponseRequest, config)

    :param string               url:                               request url
    :param Function             callback:                          response callback
    :param object               fromResponseRequest:               Creates a new request using the response
    :param boolean              fromResponseRequest.base64:        if true, converts the response body to base64. (optional)
    :param string               fromResponseRequest.method:        request method (optional)
    :param object               fromResponseRequest.meta:          request extra data (optional)
    :param string               fromResponseRequest.body:          request body (optional)
    :param object               fromResponseRequest.headers:       request headers (optional)
    :param object               fromResponseRequest.cookies:       rqeuest extra cookies (optional)
    :param string               fromResponseRequest.encoding:      default encoding (optional)
    :param int                  fromResponseRequest.priority:      request priority  (optional)
    :param boolean              fromResponseRequest.dont_filter:   if true, the request don't pass on the request duplicate filter (optional)
    :param string               fromResponseRequest.formname:      FormRequest.formname parameter (optional)
    :param string               fromResponseRequest.formxpath:     FormRequest.formxpath parameter (optional)
    :param string               fromResponseRequest.formcss:       FormRequest.formcss parameter (optional)
    :param int                  fromResponseRequest.formnumber:    FormRequest.formnumber parameter (optional)
    :param object               fromResponseRequest.formdata:      FormRequest.formdata parameter (optional)
    :param object               fromResponseRequest.clickdata:     FormRequest.clickdata parameter (optional)
    :param boolean              fromResponseRequest.dont_click:    FormRequest.dont_click parameter (optional)
    :param object               config:                            object with extra request parameters (optional)
    :param boolean              config.base64:                     if true, converts the response body to base64. (optional)
    :param string               config.method:                     request method (optional)
    :param object               config.meta:                       request extra data (optional)
    :param string               config.body:                       request body (optional)
    :param object               config.headers:                    request headers (optional)
    :param object               config.cookies:                    request extra cookies (optional)
    :param string               config.encoding:                   default encoding (optional)
    :param int                  config.priority:                   request priority  (optional)
    :param boolean              config.dont_filter:                if true, the request don't pass on the request duplicate filter (optional)

This function creates a request, and then use its response to open a new request using the :message:`from_response_request` message.

Usages:

.. code-block:: js

    var callback = function(response) {
        // parse the response
    };

    // submit a login form, first requesting the login page, and then submitting the form

    // we first create the form data to be sent
    var fromResponseRequest = {
        formcss: '#login_form',
        formdata: {user: 'admin', pass: '1'}
    };

    // and open the request
    scrapy.sendFromResponseRequest('http://example.com/login', callback, sendFromResponseRequest);

.. method:: runSpider([exceptionHandler])

    :param  function exceptionHandler: function to handle exceptions. Must receive a single parameter, the received json with the exception. (optional)

Starts the spider execution. This will bind the process stdin to read data from Scrapy Streaming, and process each message received.

If you want to handle the exceptions generated by Scrapy, pass a function that receives a single parameter as an argument.

By default, any exception will stop the spider execution and throw an Error.

Usage:

.. code-block:: js

    // create the spider

    ...
    scrapy.createSpiders("sample", ['http://example.com'], parse);

    // and start to listen the process stdin
    scrapy.runSpider();

    // with exception listener
    scrapy.runSpider(function(error){
        // ignores the exception
    });

Dmoz Streaming Spider with R
----------------------------

In this section, we'll implement the same spider developed in :ref:`quickstart` using the ``scrapystreaming`` package.
It's recommended that you have read the quickstart section before following this topic, to get more details about Scrapy
Streaming and the spider being developed.

We'll be using the `cheerio <https://github.com/cheeriojs/cheerio>`_ package to analyze the html content,
feel free to use any one.

We start by loading the required libraries and defining two global variables:

.. code-block:: js

    #!/usr/bin/env node

    var scrapy = require('scrapystreaming');
    var jsonfile = require('jsonfile');
    var cheerio = require('cheerio');

    var pendingRequests = 0;
    var result = {};


Then, we define two functions:

* **parse** - parse the initial page, and then open a new request to each subcategory
* **parse_cat** - parse the subcategory page, getting the links and saving it to the ``result`` variable.

.. code-block:: js

    // function to parse the response from the startUrls
    var parse = function(response) {
        // loads the html page
        var $ = cheerio.load(response.body);

        // extract subcategories
        $('#subcategories-div > section > div > div.cat-item > a').each(function(i, item) {
            scrapy.sendRequest('http://www.dmoz.org' + $(this).attr('href'), parse_cat);
            pendingRequests++;
        });
    };

    // parse the response from subcategories
    var parse_cat = function(response) {
        var $ = cheerio.load(response.body);

        // extract results
        $('div.title-and-desc a').each(function(i, item) {
            result[$(this).text().trim()] = $(this).attr('href');
        });

        pendingRequests--;
        // if there is no peding requests, save the result and close the spider
        if (pendingRequests == 0) {
            jsonfile.writeFile('outputs/dmoz_data.json', result);
            scrapy.closeSpider();
        }
    };

Notice that when using the :meth:`sendRequest`, we pass the ``parse_cat`` function as the callback.
Therefore, each response coming from  this request will execute the ``parse_cat`` function.

Finally, we start and run the spider, using:

.. code-block:: R

    scrapy.createSpider('dmoz', ["http://www.dmoz.org/Computers/Programming/Languages/Python/"], parse);
    scrapy.runSpider();

then, just save your spider and execute it using::

    scrapy streaming name_of_script.js

or::

    scrapy streaming node -a name_of_script.js
