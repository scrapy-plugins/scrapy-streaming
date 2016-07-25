Spider Examples
===============

We provide some simple examples to demonstrate how to use Scrapy Streaming features.

You can download these examples from https://github.com/aron-bordin/scrapy-streaming/tree/examples/examples

.. todo:: Update the examples URL to master

Examples
--------


1. **check_response_status** - This spider open a list of domains and check which domain is returning a valid status.
2. **extract_dmoz_links** - This example is covered in the quickstart section. It gets a list of websites with Python related articles
3. **request_image** - This demo shows how to download binary data.
4. **request_utf8** - Shows that Scrapy Streaming supports UTF8 encoding.
5. **fill_form** - This example covers the :message:`from_response_request` to fill a form with some data.

=========  ======== === ====== ========= ======
 Example    Python   R   Java   Node.js   More
=========  ======== === ====== ========= ======
    1         OK     OK   OK       OK       x
    2         OK     OK   OK       OK       x
    3         OK     OK   OK       OK       x
    4         OK     x    OK       OK       x
    5         OK     OK   OK       OK       x
=========  ======== === ====== ========= ======

* The Python examples are using the raw :ref:`protocol`, sending json strings in the stdout. It's recommended to
  follow theses examples if you are seeking a better understanding of the Scrapy Streaming behavior.
* R examples are using the ``scrapystreaming`` package, you can read the documentation here: :ref:`r`.
* Java examples are using the ``scrapystreaming`` library, you can read the documentation here: :ref:`java`
* Node.js examples are using the ``scrapystreaming`` package, you can read the documentation here: :ref:`node`

