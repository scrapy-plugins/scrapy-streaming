#! /usr/bin/env python
# coding: utf-8
from utils import *


def main():

    status = parse_json(stdin.readline())

    # we start checking if the channel is ready
    if status['status'] != 'ready':
        raise Exception("There is problem in the communication channel")

    write_line('''
        {
            "type": "spider",
            "name": "utf8",
            "start_urls": []
        }
        ''')

    write_line('''
            {
                "type": "request",
                "id": "page",
                "url": "http://httpbin.org/encoding/utf8"
            }''')
    
    response = stdin.readline()
    data = parse_json(response)

    with open('outputs/utf8.html', 'wb') as f:
        f.write(data['body'].encode('utf-8'))
    

if __name__ == '__main__':
    main()
