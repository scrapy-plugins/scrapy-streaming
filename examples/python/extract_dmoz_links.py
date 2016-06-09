#! /usr/bin/env python
from scrapy.selector import Selector
from utils import *


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
            # we check the id of the incoming response, and call a function to extract
            # the data from each page
            if msg['id'] == 'parse':
                response_parse(msg)
            elif msg['id'] == 'category':
                response_category(msg)


if __name__ == '__main__':
    main()

