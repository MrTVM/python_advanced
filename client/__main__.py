import json
import yaml
import socket
import argparse
import logging
import zlib
import hashlib

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

parser.add_argument(
    '-m', '--mode', type=str, default='w'
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
    
    
    if args.mode == 'w':
        while True:
            hash_obj = hashlib.sha256()
            hash_obj.update(
                str(datetime.now().timestamp()).encode(ENCODING)
            )

            user_action = input('Enter action name: ')
            user_value = input('Enter data to send: ')

            request = json.dumps(
                {
                    'action': user_action, 
                    'data': user_value,
                    'time': datetime.now().timestamp()
                }
            )

            sock.send(
                zlib.compress(
                    request.encode(encoding)
                )
            )
    else:
        while True:
            b_answer = sock.recv(buffersize)

            b_response = zlib.decompress(b_answer)

            response = json.loads(
                b_response.decode(encoding)
            )

            print(response)


except KeyboardInterrupt:
    logger.info('Client closed')
    sock.close()

