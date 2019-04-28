import json
import logging

from actions import resolve
from decorators import compressed
from protocol import (
    validate_request, make_response, make_400,
    make_404
)
from setting import (
    HOST, PORT, BUFFERSIZE, ENCODING 
)


@compressed
def handle_default_request(raw_request):
    request = json.loads(
        raw_request.decode(ENCODING)
    )

    action_name = request.get('action')

    if validate_request(request):
        controller = resolve(action_name)
        if controller:
            try:
                response = controller(request)
            except Exception as err:
                logging.critical(err)
                response = make_response(
                    request, 500, 'Interal server error'
                )
        else:
            logging.error(
                f'Action with name { action_name } does not exists'
            )
            response = make_404(request)
    else:
        logging.error('Request is not valid')
        response = make_400(request)

    return json.dumps(response).encode(ENCODING)

