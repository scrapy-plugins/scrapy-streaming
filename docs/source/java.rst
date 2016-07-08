Java Library
============

.. currentmodule:: java

.. todo:: publish it and add the link to maven central repository

We provide a helper library to help the development process of external spiders using Java.

It's recommended to read the :ref:`quickstart` before using this package.

Installation
------------

.. todo:: requires maven artifact

Gson
----

``scrapystreaming`` depends on `Gson <https://github.com/google/gson>`_. It's used to manipulate json data with Java.

    Gson is a Java library that can be used to convert Java Objects into their JSON representation. It can also be used to convert a JSON string to an equivalent Java object. Gson can work with arbitrary Java objects including pre-existing objects that you do not have source-code of.

We'll present the following Gson's methods:

* :meth:`toJson`
* :meth:`fromJson`

These commands may be helpful in the spider development.

You can read the official user guide `here: https://github.com/google/gson/blob/master/UserGuide.md <https://github.com/google/gson/blob/master/UserGuide.md>`_.


.. method:: toJson(Object object)


The :meth:`toJson` allows you to convert a Java object to JSON, and can be used as follows:

.. code-block:: java

    Gson gson = new Gson();
    gson.toJson(1);            // ==> 1
    gson.toJson("abcd");       // ==> "abcd"
    gson.toJson(new Long(10)); // ==> 10
    int[] values = { 1 };
    gson.toJson(values);       // ==> [1]

.. method:: fromJson(String json, Class klass)


You can use the :meth:`fromJson` command to converts a json string to a Java object again.

.. code-block:: java

    int one = gson.fromJson("1", int.class);
    Integer one = gson.fromJson("1", Integer.class);
    Long one = gson.fromJson("1", Long.class);
    Boolean false = gson.fromJson("false", Boolean.class);
    String str = gson.fromJson("\"abc\"", String.class);
    String[] anotherStr = gson.fromJson("[\"abc\"]", String[].class);


You can read more advanced examples in the `Gson user guide: https://github.com/google/gson/blob/master/UserGuide.md <https://github.com/google/gson/blob/master/UserGuide.md>`_.

If you prefer, you can access a gson instance from ``org.scrapy.scrapystreaming.utils.Utils.gson``.


scrapystreaming
---------------


The ``scrapystreaming`` library provide the following objects:


* :class:`Spider`
* :class:`Callback`
* :class:`SpiderException`
* :class:`Request`
* :class:`FromResponseMessage`
* :class:`FromResponseRequest`
* :class:`Logger`


.. class:: Spider

    *(org.scrapy.scrapystreaming.Spider)*

    This class defines your spider.

    To implement a Spider, extends this class and implements the :meth:`parse` method.

    .. attribute:: name

        *(String)* The name of the Spider, defaults to ``ExternalSpider``.

    .. attribute:: start_urls

        *(List<String>)* Initial URLs, defaults to an empty array list.

    .. attribute:: allowed_domains

        *(List<String>)* Allowed domains, defaults to null.

    .. attribute:: custom_settings

        *(Map)* Spider custom settings, defaults to null.

    .. method:: start()

        *(void)* Initializes the Spider execution. Throws :class:`SpiderException`.

    .. method:: close()

        *(void)* Sends a :message:`close` message to stops the Spider execution.

    .. method:: parse(ResponseMessage response)

        *(abstract void)* This method must be implemented to parse the response from initial URLs.

    .. method:: onException(ExceptionMessage exception)

        *(void)* This method is called when Scrapy raises an exception and sends the exception message.
        If you want to analyze the exception, or just ignore the problem, override this function.

        Throws :class:`SpiderException`.


.. class:: Callback

    *(org.scrapy.scrapystreaming.core.Callback)*

    Callback is an interface to handle responses. The :class:`Spider` implements this interface, and you need
    to provide a callback instance to open new requests.

    .. method:: parse(ResponseMessage response)

        (void) Method to handle to response content

.. class:: SpiderException

    *(org.scrapy.scrapystreaming.core.SpiderException)*

    Exceptions raised by Scrapy Streaming and Scrapy

.. class:: Request

    *(org.scrapy.scrapystreaming.Request)*

    Class responsible for creating new requests.

    .. method:: Request(String url)

        Creates the Request object with a given URL

    .. method:: open(Callback callback)

        *(void)* Opens the request, and parse the response in the callback instance.

        The callback can be any class that implements the :class:`Callback` interface, including the spider instance.

        Throws :class:`SpiderException`.

.. class:: FromResponseMessage

    *(org.scrapy.scrapystreaming.messages.FromResponseMessage)*

    This is a simple class to put extra data to :class:`FromResponseRequest` requests.

    .. attribute:: formname

        *(String)* FromResponseRequest's formname parameter

    .. attribute:: formxpath

        *(String)* FromResponseRequest's formxpath parameter

    .. attribute:: formcss

        *(String)* FromResponseRequest's formcss parameter

    .. attribute:: formnumber

        *(Integer)* FromResponseRequest's formnumber parameter

    .. attribute:: formdata

        *(Map)* FromResponseRequest's formdata parameter

    .. attribute:: clickdata

        *(Map)* FromResponseRequest's clickdata parameter

    .. attribute:: dont_click

        *(Boolean)* FromResponseRequest's dont_click parameter


.. class:: FromResponseRequest

    *(org.scrapy.scrapystreaming.Request)*

    Class responsible for creating new requests using response and extra data.

    .. method:: FromResponseRequest(String url, FromResponseMessage from_response_request)

        Creates the FromResponseRequest object with a given URL, using the :class:`FromResponseMessage` data.

    .. method:: open(Callback callback)

        *(void)* Opens the request, and parse the response in the callback instance.

        The callback can be any class that implements the :class:`Callback` interface, including the spider instance.

        Throws :class:`SpiderException`.

.. class:: Logger

    *(org.scrapy.scrapystreaming.Logger)*

    The Logger class lets you write log messages in the Scrapy Streaming logger.

    .. classmethod:: log(String message, LEVEL level)

        *(void)* Write a log message.

        LEVEL is a enum defined in ``Logger.LEVEL``, and can be CRITICAL, ERROR, WARNING, INFO, or DEBUG.

    .. classmethod:: critical(String message)

        *(void)* Write a critical message in the Scrapy Streaming logger.

    .. classmethod:: error(String message)

        *(void)* Write a error message in the Scrapy Streaming logger.

    .. classmethod:: warning(String message)

        *(void)* Write a warning message in the Scrapy Streaming logger.

    .. classmethod:: info(String message)

        *(void)* Write a info message in the Scrapy Streaming logger.

    .. classmethod:: debug(String message)

        *(void)* Write a debug message in the Scrapy Streaming logger.

Dmoz Streaming Spider with Java
-------------------------------

In this section, we'll implement the same spider developed in :ref:`quickstart` using the ``scrapystreaming`` java library.
It's recommended that you have read the quickstart section before following this topic, to get more details about Scrapy
Streaming and the spider being developed.

We'll be using the `jsoup selector <https://jsoup.org/cookbook/extracting-data/selector-syntax>`_ to analyze the html content,
feel free to use any one.

We start by defining the Spider class and creating two variables:

.. code-block:: java

    public class Dmoz extends Spider {
        // we use the numRequests to count remaining requests
        static int numRequests = 0;
        // the results variable store the extracted data, mapping from title: url
        static HashMap<String, String> results = new HashMap<String, String>(0);

        Dmoz() {
            name = "dmoz";
            // set the initial url
            start_urls.add("http://www.dmoz.org/Computers/Programming/Languages/Python/");
        }


Then, we must implement the :meth:`Spider.parse` method to handle the response from start_urls requests:

.. code-block:: java

    public void parse(ResponseMessage response) {
        // get the initial page, and open a new request to each subcategory
        Document doc = Jsoup.parse(response.body);
        Elements hrefs = doc.select("#subcategories-div > section > div > div.cat-item > a[href]");
        for (Element el: hrefs) {
            try {
                Request r = new Request("http://www.dmoz.org" + el.attr("href"));
                r.open(new Callback() {
                    public void parse(ResponseMessage response) {
                        parseSubcat(response);
                    }
                });

                // increments the number of open requests
                numRequests++;
            } catch (SpiderException e) {
                e.printStackTrace();
            }
        }
    }


This method get external links usign the jsoup selector, and increment the ``numRequests`` variables,
so we can keep trace of the number of webpages being extracted.

We create a new request to each link found, and the get the response using the :class:`Callback` object,
and the calling the ``parseSubcat`` method.


.. tip:: If instead of creating a new :class:`Callback` object to each request,
         you can pass a single object that implements the callback interface, or just pass the spider instance.

Now, let's implement the ``parseSubcat`` method.

.. code-block:: java

    public void parseSubcat(ResponseMessage response) {
        // decrement the number of open requests
        numRequests--;
        Document doc = Jsoup.parse(response.body);
        Elements divs = doc.select("div.title-and-desc a");

        // extract all urls in the page
        for (Element item: divs) {
            String url = item.attr("href");
            String title = item.select("div.site-title").first().text();
            results.put(title, url);
        }

        // close the spider and save the data, when necessary
        if (numRequests == 0) {
            try {
                Writer writer = new FileWriter("outputs/dmoz.json");
                Utils.gson.toJson(results, writer);
                writer.flush();
            } catch (Exception e) {
                e.printStackTrace();
            }
            close();
        }
    }

The ``parseSubcat`` method first extract the external link title and href, and then adds it to the results variable.

When there is no response remaining (numRequests is equal to 0), the extracted data is converted to json and written in the disk.

Following that, the :meth:`Spider.close` is called, to close the spider.

Finally, we add a main method to make this spider executable.

.. code-block:: java

    public static void main(String args[]) throws Exception {
        Dmoz spider = new Dmoz();
        spider.start();
    }


To execute the spider, you can use something similar to::

    scrapy streaming java -a -cp,.:\*,Dmoz

Where ``-a`` means that we are adding some arguments to the java command.
The arguments used here are:

    * -cp,.:\\* to add the required .jars in the java classpath (if you have both scrapystreaming and its dependencies in the java classpath, you can skip this parameter)
    * a comma, to separate the next argument
    * Dmoz, the name of the class
