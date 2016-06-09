Quickstart - Dmoz Streaming Spider
==================================

In this tutorial, we’ll assume that both Scrapy and Scrapy Streaming is already installed on your system.
If that’s not the case, see :ref:`installation`.

We'll develop the spider using Python because its simplicity, however, you can implement it using any programming language
using the necessary syntax modifications.

In this tutorial, we'll implement a simple spider to extract data from http://www.dmoz.org.

Spider Behavior
---------------

If you are not familiar with Scrapy, we name Spider as an object that defines how scrapy should scrape
information from a domain (or a group of domains). It contains the all the logic and necessary information to
extract the data from a website.

We'll define a simple spider, that works as follows:

- The spider initializes at http://www.dmoz.org/Computers/Programming/Languages/Python/
- For each subcategory in ``Subcategories`` section, we need to open its page, and extract the link of external websites in the ``Sites`` section.
- Extracted values will be saved in a dictionary that maps ``title: url``.

Scrapy Streaming
----------------

The Scrapy Streaming plugin uses the default ``stdin`` and ``stdout`` to communicate with Scrapy. This means that
you must have Scrapy installed on your system to use it with the plugin.

Scrapy will be responsible for starting your process (defined as external spider) and create a communication
channel that uses json messages.

Therefore, the spider can be implemented in any programming language as long as it supports communication with the
system ``stdin`` and ``stdout``.

Dmoz Spider Implementation
--------------------------

Now we'll implement the sample spider using Python language. Read the :ref:`protocol` for more information about
it.

Each message ends with a line break ``\n``, so it's important to read and send a single message per line.

After starting your process, Scrapy'll let it know that the communication channel is ready sending the following
message:

.. code-block:: python

    {
        "type": "status",
        "status": "ready"
    }

So, the first thing is to wait the scrapy's confirmation. We start implementing as follows:

.. code-block:: python
    :caption: dmoz_spider.py
    :linenos:
    :emphasize-lines: 27

    #! /usr/bin/env python
    import json
    from sys import stdin, stdout
    from scrapy.selector import Selector


    def parse_json(line):
        # parses the line string to a python object
        return json.loads(line)


    def write_line(data):
        # converts data to a single line message and write it in the system stdout
        msg = ''.join([line.strip() for line in data.splitlines()])
        stdout.write(msg + '\n')

    pending_requests = 0
    result = {}

    def main():
        status = parse_json(stdin.readline())

        # we start checking if the channel is ready
        if status['status'] != 'ready':
            raise Exception("There is problem in the communication channel")

        # continue with the implementation here

    if __name__ == '__main__':
        main()

We read the line from system ``stdin`` and confirms that it's a :message:`status` ready confirmation.

The code above defines two helper functions, ``parse_json`` that receives an string and convert it to a python
object (a dict); and ``write_line`` that receives a multiline string and convert it to a single-line one, and write
it to the ``stdout`` with a line-break.

Now, we must provide the :message:`spider` information. On line ``27``, a spider is defined adding the following code:

.. code-block:: python

    write_line('''
        {
            "type": "spider",
            "name": "dmoz",
            "start_urls": ["http://www.dmoz.org/Computers/Programming/Languages/Python/"]
        }
    ''')

With this message, the scrapy steaming will create a Spider and start its execution, requesting the
``start_urls`` pages.

After the ``write_line`` call, we implement a loop that will be always checking the system ``stdin``.
This loop will check if the spider got some problems in the execution, and analyze the responses.

We define the main loop as:

.. code-block:: python

    while True:
        msg = parse_json(stdin.readline())

        # check the message type
        if msg['type'] == 'exception' or msg['type'] == 'error':
            raise Exception("Something wrong... " + str(msg))

        elif msg['type'] == 'response':
            # we check the id of the incoming response, and call a function to extract
            # the data from each page
            if msg['id'] == 'parse':
                response_parse(msg)
            elif msg['id'] == 'category':
                response_category(msg)

The code above start checking if there is some problem in the spider, and then check it's a response.

Our spider will have two type of responses:

- **parse**: this is sent after receiving the content from ``start_urls``
- **category**: this is sent after receiving the content of each subcategory (we'll implement it soon)

Responses that has the ``id`` field equals to ``parse`` comes from the ``start_urls`` requests.
So, let's start implementing the ``response_parse`` method. This method will get a list of subcategories
at http://www.dmoz.org/Computers/Programming/Languages/Python/ and open a new request to each subcategory page.

Let's implement the ``response_parse`` function. This function receives the response from the initial
url and open a new request to each repository.

.. code-block:: python

    def response_parse(response):
        global pending_requests
        # using scrapy selector to extract data from the html
        selector = Selector(text=response['body'])
        # get the url of subcategories
        for href in selector.css("#subcategories-div > section > div > div.cat-item > a::attr('href')"):
            # we count the number of requests using this var
            pending_requests += 1
            # open a new request
            write_line('''
                {
                    "type": "request",
                    "id": "category",
                    "url": "http://www.dmoz.org%s"
                }
            ''' % href.extract())

We are using scrapy's Selector to extract data from the html body, but feel free to use anyone. For each
subcategory html, we open a new request using the write_line with the :message:`request` message. Notice that
these requests are using the ``id`` equals to ``category``, so its responses will have a field with the same value.

Finally, let's implement the ``response_category`` method. This method receives the response of each subcategory.

.. code-block:: python

    def response_category(response):
        global pending_requests
        # this response is no longer pending
        pending_requests -= 1

        # using scrapy selector
        selector = Selector(text=response['body'])
        # get div with link and title
        divs = selector.css('div.title-and-desc')

        for div in divs:
            url = div.css("a::attr('href')").extract_first();
            title = div.css("a > div.site-title::text").extract_first();
            result[title] = url

        # if finished all requests, we can close the spider
        if pending_requests == 0:
            # serialize the extracted data and close the spider
            open('outputs/dmoz_data.json', 'w').write(json.dumps(result))
            write_line('{"type": "close"}')


For each response received, we decrease the ``pending_requests`` value, and the we close the spider when there
is no pending request.

Now, to run your spider use the following command::

    scrapy streaming dmoz_spider.py

This command will start your process and run your spider until receive the :message:`close` message.

Source code
-----------

The source used in this section:

.. code-block:: python
    :linenos:

    #! /usr/bin/env python
    import json
    from sys import stdin, stdout
    from scrapy.selector import Selector


    def parse_json(line):
        # parses the line string to a python object
        return json.loads(line)


    def write_line(data):
        # converts data to a single line message and write it in the system stdout
        msg = ''.join([line.strip() for line in data.splitlines()])
        stdout.write(msg + '\n')
        stdout.flush()

    pending_requests = 0
    result = {}


    def response_parse(response):
        global pending_requests
        # using scrapy selector to extract data from the html
        selector = Selector(text=response['body'])
        # get the url of repositories
        for href in selector.css("#subcategories-div > section > div > div.cat-item > a::attr('href')"):
            # we count the number of requests using this var
            pending_requests += 1
            # open a new request
            write_line('''
                {
                    "type": "request",
                    "id": "category",
                    "url": "http://www.dmoz.org%s"
                }
            ''' % href.extract())


    def response_category(response):
        global pending_requests
        # this response is no longer pending
        pending_requests -= 1

        # using scrapy selector
        selector = Selector(text=response['body'])
        # get div with link and title
        divs = selector.css('div.title-and-desc')

        for div in divs:
            url = div.css("a::attr('href')").extract_first();
            title = div.css("a > div.site-title::text").extract_first();
            result[title] = url

        # if finished all requests, we can close the spider
        if pending_requests == 0:
            # serialize the extracted data and close the spider
            open('outputs/dmoz_data.json', 'w').write(json.dumps(result))
            write_line('{"type": "close"}')


    def main():
        status = parse_json(stdin.readline())

        # we start checking if the channel is ready
        if status['status'] != 'ready':
            raise Exception("There is problem in the communication channel")

        write_line('''
            {
                "type": "spider",
                "name": "dmoz",
                "start_urls": ["http://www.dmoz.org/Computers/Programming/Languages/Python/"]
            }
        ''')

        while True:
            msg = parse_json(stdin.readline())

            # check the message type
            if msg['type'] == 'exception' or msg['type'] == 'error':
                raise Exception("Something wrong... " + str(msg))

            elif msg['type'] == 'response':
                # we check the id of the incoming response, and call a funtion to extract
                # the data from each page
                if msg['id'] == 'parse':
                    response_parse(msg)
                elif msg['id'] == 'category':
                    response_category(msg)


    if __name__ == '__main__':
        main()
