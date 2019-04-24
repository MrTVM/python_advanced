import json
import yaml
import socket
import argparse
import logging


from setting import (
    ENCODING, HOST, PORT, BUFFERSIZE
)
from actions import(
    resolve, get_server_actions
)
from protocol import (
    validate_request, make_response, make_400, 
    make_404
)


def check_validate(request, server_actions):
    action_name = request.get('action')
    
    if validate_request(request):
        controller = resolve(action_name, server_actions)
        if controller:
            try:
                return controller(request)
            except Exception as err:
                logger.critical(err)
                return make_response(
                    request, 500, 'Internal server error'
                )
        else:
            logger.error(f'Action with name { action_name } does not exists')
            return make_404(request)
    else:
        logger.error('Request is not valid')
        return make_400(request)


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
    sock.bind((host, port))
    sock.listen(5)
    server_actions = get_server_actions()

    logger.info('Server started')

    while True:
        client, address = sock.accept()

        logger.info(f'Client with address { address } was detected')

        b_request = client.recv(buffersize)
        request = json.loads(b_request.decode(encoding))

        response = check_validate(request, server_actions)

        s_response = json.dumps(response)
        client.send(s_response.encode(encoding))
        
        client.close()
except KeyboardInterrupt:
    logger.info('Server closed')

