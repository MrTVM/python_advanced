import json
from socket import socket
from typing import List

import yaml
import socket
import select
import argparse
import logging


from setting import (
    ENCODING, HOST, PORT, BUFFERSIZE
)
from handlers import handle_default_request


encoding = ENCODING
host = HOST
port = PORT
buffersize = BUFFERSIZE
file_name = 'server.log'

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


logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler(file_name, encoding=ENCODING),
        logging.StreamHandler()
    ]
)


requests = []
connections = []

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.settimeout(0.1)
    sock.listen(10)

    logging.info('Server started')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client with address { address } was detected')
            connections.append(client)
        except:
            pass

        if connections:
            rlist, wlist, xlist = select.select(connections, connections, connections, 0.1)
        else:
            rlist, wlist, xlist = [], [], []

        for r_client in rlist:
            b_request =r_client.recv(buffersize)
            requests.append(b_request)

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_client.send(b_response)
        
except KeyboardInterrupt:
    logging.info('Client closed')

