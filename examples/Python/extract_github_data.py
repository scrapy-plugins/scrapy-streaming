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
    for href in selector.css("h3.repo-list-name > a::attr('href')"):
        # we count the number of requests using this var
        pending_requests += 1
        # open a new request
        write_line('''
            {
                "type": "request",
                "id": "repo",
                "url": "https://github.com%s"
            }
        ''' % href.extract())


def response_repo(response):
    global pending_requests
    # this response is no longer pending
    pending_requests -= 1

    # using scrapy selector
    selector = Selector(text=response['body'])
    # get the desired field
    title = selector.css('h1.public strong a::text').extract_first()
    stars = int(selector.css('a.social-count::text').extract()[1])
    issues = int(selector.css('span.counter::text').extract()[0])
    pr = int(selector.css('span.counter::text').extract()[1])
    item = {
        'title': title,
        'stars': stars,
        'issues': issues,
        'pr': pr
    }
    # save the extracted data on a variable name result
    result[title] = item

    # if finished all requests, we can close the spider
    if pending_requests == 0:
        # serialize the extracted data and close the spider
        open('outputs/github_data.json', 'w').write(json.dumps(result))
        write_line('{"type": "close"}')


def main():
    status = parse_json(stdin.readline())

    # we start checking if the channel is ready
    if status['status'] != 'ready':
        raise Exception("There is problem in the communication channel")

    write_line('''
        {
            "type": "spider",
            "name": "github",
            "start_urls": ["https://github.com/scrapy-plugins"]
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
            elif msg['id'] == 'repo':
                response_repo(msg)


if __name__ == '__main__':
    main()
