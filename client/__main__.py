import json
import yaml
import socket
import argparse
import logging

from datetime import datetime
from setting import (
    ENCODING, HOST, PORT, BUFFERSIZE
)

encoding = ENCODING
host = HOST
port = PORT
buffersize = BUFFERSIZE
file_name = 'client.log'

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

logger = logging.getLogger('main')

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

handler = logging.FileHandler(file_name, encoding=encoding)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

try:
    sock = socket.socket()
    sock.connect((host, port))
    
    logger.info('Server started')

    user_action = input('Enter action name: ')
    user_value = input('Enter data to send: ')
    
    request = json.dumps(
        {
            'action': user_action, 
            'data': user_value,
            'time': datetime.now().timestamp()
        }
    )

    sock.send(request.encode(encoding))
    b_answer = sock.recv(buffersize)
    response = json.loads(
        b_answer.decode(encoding)
    )

    if response.get('code') == 200:
        print(response)
    elif response.get('code') == 400:
        print('Request is not valid')
        logger.error('Request is not valid')
    elif response.get('code') == 404:
        print(f'Action with name { user_action } does not exists')
        logger.error(f'Action with name { user_action } does not exists')

    sock.close()
except KeyboardInterrupt:
    logger.info('Client closed')

