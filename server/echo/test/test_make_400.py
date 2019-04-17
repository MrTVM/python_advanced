from datetime import datetime
from server.protocol import make_400


def test_make_400():
    request = {
        'action': 'echo',
        'time': datetime.now().timestamp(),
        'data': 'some data'
    }
    return make_400(request)


print(test_make_400())

