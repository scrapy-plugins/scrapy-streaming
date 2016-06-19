#! /usr/bin/env python
import sys

if __name__ == '__main__':
    status = sys.stdin.readline()
    sys.stdout.write('{"type": "log", "level": "debug", "message": "qwertyuiop"}\n' * 1000)
    sys.stdout.flush()
    sys.stdout.write('{"type": "close"}' * 10)
    sys.stdout.flush()
