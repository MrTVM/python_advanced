import json
from socket import socket
from typing import List

import yaml
import socket
import select
import argparse
import logging
import threading


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


def read(client, requests, buffersize):
    b_request = client.recv(buffersize)
    requests.append(b_request)


def write(client, response):
    client.send(response)


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
            r_tread = threading.Thread(
                target=read,
                args=(r_client, requests, buffersize),
                daemon=True
            )
            r_tread.start()

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_thread = threading.Thread(
                    target=write,
                    args=(w_client, b_response),
                    daemon=True
                )
                w_thread.start()
        
except KeyboardInterrupt:
    logging.info('Client closed')

