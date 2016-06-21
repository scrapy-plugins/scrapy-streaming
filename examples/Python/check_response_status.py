#! /usr/bin/env python
from utils import *


requests = {
    '200': None,
    '201': None,
    '400': None,
    '404': None,
    '500': None
}


def main():
    status = parse_json(stdin.readline())

    # we start checking if the channel is ready
    if status['status'] != 'ready':
        raise Exception("There is problem in the communication channel")

    write_line('''
        {
            "type": "spider",
            "name": "status",
            "start_urls": []
        }
        ''')
        
    pending_requests = len(requests)
    
    for k in requests.keys():
        write_line('''
            {
                "type": "request",
                "id": "%s",
                "url": "http://httpbin.org/status/%s"
            }''' % (k, k))
            
    while pending_requests:
        msg = parse_json(stdin.readline())

        # check the message type
        if msg['type'] == 'exception':
            sent_message = json.loads(msg['received_message'])
            requests[sent_message['id']] = False
            pending_requests -= 1
        elif msg['type'] == 'response':
            # validate if the incoming status is correct

            assert int(msg['id']) == msg['status']
            requests[msg['id']] = True
            pending_requests -= 1
            
    open('outputs/response_status.json', 'w').write(json.dumps(requests))
    write_line('{"type": "log", "level": "debug", "message": "DONE"}\n')
    write_line('{"type": "close"}')
    
if __name__ == '__main__':
    main()
