import json
import yaml
import socket
import argparse
from setting import (
    ENCODING, HOST, PORT, BUFFERSIZE
)

encoding = ENCODING
host = HOST
port = PORT
buffersize = BUFFERSIZE

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration'
)

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        conf = yaml.load(file, Loader=yaml.Loader)
        host = conf.get('host', host)
        port = conf.get('port', port)
        buffersize = conf.get('buffersize', buffersize)

try:
    sock = socket.socket()
    sock.connect((host, port))
    
    print('Client started')

    user_value = input('Enter data to send: ')
    request = json.dumps(
        {'data': user_value}
    )

    sock.send(request.encode(encoding))
    b_answer = sock.recv(buffersize)
    response = json.loads(
        b_answer.decode(encoding)
    )

    print(response)

    sock.close()
except KeyboardInterrupt:
    print('Client closed')

