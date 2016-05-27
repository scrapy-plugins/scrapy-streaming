#! /usr/bin/env python
import sys

if __name__ == '__main__':
    status = sys.stdin.readline()
    sys.stdout.write('{"type": "log", "level": "debug", "message": "sample1.py working"}\n')
