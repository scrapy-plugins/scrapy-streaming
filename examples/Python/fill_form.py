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
            "name": "form",
            "start_urls": []
        }
        ''')

    write_line('''
            {
                "type": "from_response_request",
                "id": "form",
                "url": "http://httpbin.org/forms/post",
                "from_response_request": {
                    "formdata": {
                        "custname": "Sample",
                        "custemail": "email@example.com"
                    }
                }
            }''')

    response = stdin.readline()
    data = parse_json(response)

    with open('outputs/fill_form.json', 'w') as f:
        f.write(data['body'])
        f.flush()


if __name__ == '__main__':
    main()
