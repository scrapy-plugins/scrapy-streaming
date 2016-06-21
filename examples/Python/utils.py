import simplejson as json
from sys import stdin, stdout
import os

if not os.path.exists('outputs'):
    os.mkdir('outputs')


def parse_json(line):
    # parses the line string to a python object
    return json.loads(line)


def write_line(data):
    # converts data to a single line message and write it in the system stdout
    msg = ''.join([line.strip() for line in data.splitlines()])
    stdout.write(msg + '\n')
    stdout.flush()
