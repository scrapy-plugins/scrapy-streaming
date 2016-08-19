#! /usr/bin/env python
from utils import *
import base64


def main():
    status = parse_json(stdin.readline())

    # we start checking if the channel is ready
    if status['status'] != 'ready':
        raise Exception("There is problem in the communication channel")

    write_line('''
        {
            "type": "spider",
            "name": "image",
            "start_urls": []
        }
        ''')

    write_line('''
            {
                "type": "request",
                "id": "file",
                "url": "http://httpbin.org/image/png",
                "base64": true
            }''')

    msg = parse_json(stdin.readline())

    # check the message type
    if msg['type'] == 'exception':
        raise Exception("Failed to get content")
    elif msg['type'] == 'response':

        img = base64.b64decode(msg['body'])
        with open('outputs/image.png', 'wb') as f:
            f.write(img)
        write_line('{"type": "log", "level": "debug", "message": "DONE"}')

    write_line('{"type": "close"}')

if __name__ == '__main__':
    main()
