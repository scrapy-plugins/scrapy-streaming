.. _r:

R Package
=========
.. currentmodule:: R


.. todo:: publish it and add the link to cran package with the package docs here

We provide a helper library to help the development process of external spiders in R.

It's recommended to read the :ref:`quickstart` before using this package.

Installation
------------

To install the ``scrapystreaming`` package, runs:

.. code-block:: R

    install.packages("scrapystreaming")

and loads it using:

.. code-block:: R

    library(scrapystreaming)

jsonlite
--------

``scrapystreaming`` will load the `jsonlite <https://cran.r-project.org/web/packages/jsonlite/index.html>`_ package.

    The jsonlite package offers flexible, robust, high performance tools for working with JSON in R and is particularly powerful for building pipelines and interacting with a web API.

We focus our attention to two jsonlite's commands:

* :meth:`toJSON`
* :meth:`fromJSON`

These commands may be helpful in the spider development.

You can read the jsonlite's quickstart here: https://cran.r-project.org/web/packages/jsonlite/vignettes/json-aaquickstart.html
and a more detailed documentation here: http://arxiv.org/abs/1403.2805


.. method:: toJSON(x, dataframe = c("rows", "columns", "values"), matrix = c("rowmajor", "columnmajor"), Date = c("ISO8601", "epoch"), POSIXt = c("string", "ISO8601", "epoch", "mongo"), factor = c("string", "integer"), complex = c("string", "list"), raw = c("base64", "hex", "mongo"), null = c("list", "null"), na = c("null", "string"), auto_unbox = FALSE, digits = 4, pretty = FALSE, force = FALSE, ...)


The :meth:`toJSON` allows you to convert a R object to JSON, and can be used as follows:

.. code-block:: R

    > test1 <- data.frame(a = "a field", b = 2)
    > toJSON(test1)
    [{"a":"a field","b":2}]
    >
    > nested_data <- data.frame(user = "admin", pass = "secret")
    > data <- data.frame(login = "ok", attempts = 2, input = NA)
    > data$input <- nested_data
    > toJSON(data)
    [{"login":"ok","attempts":2,"input":{"user":"admin","pass":"secret"}}]

.. method:: fromJSON(txt, simplifyVector = TRUE, simplifyDataFrame = simplifyVector, simplifyMatrix = simplifyVector, flatten = FALSE, ...)

You can use the :meth:`fromJSON` command to converts a json string to a R object again.

.. code-block:: R

    > converted_test1 <- fromJSON('[{"a":"a field","b":2}]')
    > converted_data <- fromJSON('[{"login":"ok","attempts":2,"input":{"user":"admin","pass":"secret"}}]')


scrapystreaming
---------------


The ``scrapystreaming`` R package provide the following commands:

* :meth:`create_spider`
* :meth:`close_spider`
* :meth:`send_log`
* :meth:`send_request`
* :meth:`send_from_response_request`
* :meth:`parse_input`
* :meth:`handle`
* :meth:`run_spider`

.. tip:: The Scrapy Streaming and your spider communicates using the system ``stdin``, ``stdout``, and ``stderr``.
         So, don't write any data that is not a json message to the system ``stdout`` or ``stderr``.

         These commands write and read data from ``stdin``, ``stdout``, and ``stderr`` when necessary, so you don't need to handle
         the communication channel manually.

.. method:: create_spider(name, start_urls, [callback, allowed_domains, custom_settings])

    :param character    name:              The name of the spider
    :param character    start_urls:        vector with initial urls
    :param function     callback:          the function to handle the response callback from start_urls requests, must receive one parameter ``response`` that is a data.frame with the response data
    :param character    allowed_domains:   vector with allowed domains (optional)
    :param data.frame   custom_settings:   custom scrapy settings (optional)

This command is used to create and run a Spider, sending the :message:`spider` message.

Usages:

.. code-block:: R

    parse <- function (response) {
        # do something with response
    }

    # usage 1, all parameters
    create_spider(name = "sample",
                  start_urls = "http://example.com",
                  allowed_domains = c("example.com", "dmoz.org"),
                  callback = parse,
                  custom_settings = data.frame("SOME_SETTING" = "some value"))

    # usage 2, empty spider
    create_spider(name = "sample", start_urls = character(0))

.. method:: close_spider()

Closes the spider, sending the :message:`close` message.

Usage:

.. code-block:: R

    close_spider()


.. method:: send_log(message, level = "DEBUG")

    :param character message:  the log message
    :param character level:    log level. Must be one of 'CRITICAL', 'ERROR', 'WARNING', 'DEBUG', and 'INFO', defaults to DEBUG

Send a log message to the Scrapy Streaming's logger output. This commands sends the :message:`log` message.

Usages:

.. code-block:: R

    # default DEBUG message
    send_log("starting spider")

    # logging some error
    send_log("something wrong", "error")

.. method:: send_request(url, callback, [base64, method, meta, body, headers, cookies, encoding, priority, dont_filter])

    :param character url:           request url
    :param function callback:       the function to handle the response callback, must receive one parameter ``response`` that is a data.frame with the response data
    :param logical base64:          if TRUE, the response body will be encoded with base64 (optional)
    :param character method:        request method (optional)
    :param data.frame meta:         metadata to the request (optional)
    :param character body:          the request body (optional)
    :param data.frame headers:      request headers (optional)
    :param data.frame cookies:      request cookies  (optional)
    :param character encoding:      request encoding  (optional)
    :param numeric priority:        request priority  (optional)
    :param logical dont_filter:     indicates that this request should not be filtered by the scheduler (optional)


Open a new request, using the :message:`request` message.

Usages:

.. code-block:: R

    my_callback <- function (response) {
        # do something with response
    }

    # simple request
    send_request("http://example.com", my_callback)

    # base64 encoding, used to request binary content, such as files
    send_request("http://example.com/some_file.xyz", my_callback, base64 = TRUE)

.. method:: send_from_response_request(url, callback, from_response_request, [base64, method, meta, body, headers, cookies, encoding, priority, dont_filter])

    :param character     url:                                       request url
    :param function      callback:                                  the function to handle the response callback, must receive one parameter ``response`` that is a data.frame with the response data

    :param data.frame    from_response_request:                     data to the new request. May contain fields to the request and to the form.
    :param character     from_response_request$method:              request method (optional)
    :param data.frame    from_response_request$meta:                metadata to the request (optional)
    :param character     from_response_request$body:                the request body (optional)
    :param data.frame    from_response_request$headers:             request headers (optional)
    :param data.frame    from_response_request$cookies:             request cookies  (optional)
    :param character     from_response_request$encoding:            request encoding  (optional)
    :param numeric       from_response_request$priority:            request priority  (optional)
    :param logical       from_response_request$dont_filter:         indicates that this request should not be filtered by the scheduler (optional)

    :param logical       base64:                                    if TRUE, the response body will be encoded with base64 (optional)
    :param character     method:                                    request method (optional)
    :param data.frame    meta:                                      metadata to the request (optional)
    :param character     body:                                      the request body (optional)
    :param data.frame    headers:                                   request headers (optional)
    :param data.frame    cookies:                                   request cookies  (optional)
    :param character     encoding:                                  request encoding  (optional)
    :param numeric       priority:                                  request priority  (optional)
    :param logical       dont_filter:                               indicates that this request should not be filtered by the scheduler (optional)


This function creates a request, and then use its response to open a new request using the :message:`from_response_request` message.

Usages:

.. code-block:: R

    my_callback <- function (response) {
        # do something with response
    }

    # submit a login form, first requesting the login page, and then submitting the form

    # we first create the form data to be sent
    from_response_request <- data.frame(formcss = character(1), formdata = character(1))
    from_response_request$formcss <- "#login_form"
    from_response_request$formdata <- data.frame(user = "admin", pass = "1")

    # and open the request
    send_from_response_request("http://example.com/login", my_callback, from_response_request)

.. method:: parse_input(raw = FALSE, ...)

    :param logical raw: if TRUE, returns the raw input line. If FALSE (the default), parse it using jsonlite::fromJSON (optional)
    :param ...:         extra arguments to jsonlite::fromJSON (optional)

This method reads the ``stdin`` data.

If raw is equal to TRUE, returns the string of one line received.

Otherwise, it will parse the line using :meth:`fromJSON`, with `...` as argument.

Usages:

.. code-block:: R

    # raw message
    line <- parse_input(raw = TRUE)

    # json message
    msg <- parse_input()

    # message with custom toJSON parameters
    msg <- parse_input(FALSE, simplifyVector = FALSE, simplifyDataFrame = FALSE)

.. method:: handle(execute = TRUE)

    :param logical execute: if TRUE (the default) will execute the message as follows:

                            * ready: if the status is ready, continue the execution
                            * response: call the callback with the message as the first parameter
                            * error: stop the execution of the process and show the spider error
                            * exception: stop the execution of the process and show the scrapy exception

Read a line from ``stdin`` and processes it.

if false, will return the line processed with :meth:`fromJSON`.


Usages:

.. code-block:: R

    # usage 1, keep executing incoming data
    while (TRUE) {
        handle()
    }

    # usage 2, handle a single message
    # first, open the request
    send_request("http://example.com", my_callback)
    # and then processes the stdin to get the response, some exception, or errors
    handle()

.. method:: run_spider()

This method is a shortcut to always handle the incoming data. It's a simple loop that keep using the :meth:`handle`

Usage:

.. code-block:: R

    # create the spider

    ...
    create_spider("sample", c("url1", "url2", ...), parse)
    # and then keep always processing the scrapy streaming messages in the process stdin
    run_spider()

The :meth:`run_spider` is equivalent to

.. code-block:: R

    while (TRUE) {
        handle()
    }

Dmoz Streaming Spider with R
----------------------------

In this section, we'll implement the same spider developed in :ref:`quickstart` using the ``scrapystreaming`` package.
It's recommended that you have read the quickstart section before following this topic, to get more details about Scrapy
Streaming and the spider being developed.

We'll be using the `rvest <https://cran.r-project.org/web/packages/rvest/index.html>`_ package to analyze the html content,
feel free to use any one.

We start by loading the required libraries and defining two global variables:

.. code-block:: R

    #!/usr/bin/env Rscript
    suppressMessages(library(scrapystreaming))
    suppressMessages(library(rvest))

    pending_requests <- 0
    result <- list()

It's important to use the ``suppressMessages`` command to avoid unecessary data in the process stdout.

Then, we define two functions:

* **response_parse** - parse the initial page, and then open a new request to each subcategory
* **response_category** - parse the subcategory page, getting the links and saving it to the ``result`` variable.

.. code-block:: R

    # function to get the initial page
    response_parse <- function(response) {
        html <- read_html(response$body)

        for (a in html_nodes(html, "#subcategories-div > section > div > div.cat-item > a")) {
            # we count the number of requests using this var
            pending_requests <<- pending_requests + 1
            # open a new request to each subcategories
            send_request(sprintf("http://www.dmoz.org%s", html_attr(a, "href")), response_category)
        }
    }

    response_category <- function(response) {
        # this response is no longer pending
        pending_requests <<- pending_requests - 1

        html <- read_html(response$body)
        # get div with link and title
        for (div in html_nodes(html, "div.title-and-desc a")) {
            result[html_text(div, trim = TRUE)] <<- html_attr(div, "href")
        }

        # if finished all requests, we can close the spider
        if (pending_requests == 0) {
            f <- file("outputs/dmoz_data.json")
            # serialize the extracted data and close the spider
            write(toJSON(result), f)
            close(f)
            close_spider()
        }
    }

Notice that when using the :meth:`send_request`, we pass the ``parse_category`` function as the callback.
Therefore, each response coming from  this request will execute the ``parse_category`` function.

Finally, we start and run the spider, using:

.. code-block:: R

    create_spider("dmoz", "http://www.dmoz.org/Computers/Programming/Languages/Python/", response_parse)
    run_spider()

then, just save your spider and execute it using::

    scrapy streaming name_of_script.R

or::

    scrapy streaming Rscript -a name_of_script.R
