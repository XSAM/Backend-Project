import os.path
import time
import json

dir = os.path.dirname(__file__)
log_path = dir + '/server.log'

def log(*args, **kwargs):
    pattern = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(pattern, value)
    with open(log_path, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def encode_with_utf8(str):
    return str.encode('utf-8')


def decode_with_utf8(byte):
    return byte.decode('utf-8')