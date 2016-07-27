#! /usr/bin/env python
import sys

if __name__ == '__main__':
    status = sys.stdin.readline()
    sys.stdout.write('{"type": "invalid_type", "field1": "value"}\n')
    sys.stdout.flush()
