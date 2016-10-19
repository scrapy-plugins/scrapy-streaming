#! /usr/bin/env python
import sys

if __name__ == '__main__':
    status = sys.stdin.readline()
    sys.stdout.write('{"type": "spider", "start_urls": ["invalid_url_scheme"], "name": "test"}\n')
    sys.stdout.flush()
    line = sys.stdin.readline()
