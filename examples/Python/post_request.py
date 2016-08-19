#! /usr/bin/env python
from utils import *


def main():

    status = parse_json(stdin.readline())

    # we start checking if the channel is ready
    if status['status'] != 'ready':
        raise Exception("There is problem in the communication channel")

    write_line('''
        {
            "type": "spider",
            "name": "post",
            "start_urls": []
        }
        ''')

    write_line('''
            {
                "type": "request",
                "id": "post",
                "url": "http://httpbin.org/post",
                "method": "POST",
                "body": "Post data"
            }''')

    response = stdin.readline()
    data = parse_json(response)

    with open('outputs/post.json', 'w') as f:
        f.write(data['body'])
        f.flush()


if __name__ == '__main__':
    main()
