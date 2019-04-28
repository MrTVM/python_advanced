import zlib
import logging
from functools import wraps
from protocol import make_403


logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{ func.__name__ } : { request }')
        return func(request, *args, **kwargs)

    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.get('user'):
            return func(request, *args, **kwargs)
        
        return make_403(request)
    return wrapper


def compressed(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)

    return wrapper

