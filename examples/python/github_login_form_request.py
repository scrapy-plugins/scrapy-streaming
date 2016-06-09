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
            "name": "login",
            "start_urls": []
        }
        ''')

    write_line('''
            {
                "type": "form_request",
                "id": "login",
                "url": "https://github.com/login",
                "form_request": {
                    "formdata": {
                        "login": "email@example.com",
                        "password": "password"
                    }
                }
            }''')
    
    response = stdin.readline()
    data = parse_json(response)
    
    with open('outputs/login_result.json', 'w') as f:
        if 'Incorrect username or password' in data['body']:
            write_line('{"type": "log", "level": "ERROR", "message": "Invalid password"}')
            f.write('{"result": "Invalid password"}')
        else:
            write_line('{"type": "log", "level": "debug", "message": "DONE"}')
            f.write('{"result": "Correct password"}')


if __name__ == '__main__':
    main()
