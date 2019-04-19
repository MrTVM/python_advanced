from datetime import datetime
from protocol import (make_400)


def test_make_400():
    action_name = 'user'
    data = 'some data'

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
        'data': data,
    }

    expected = {
        'action': action_name,
        'user': None,
        'time': None,
        'data': data,
        'code': 400
    }

    response = make_400(request)

    assert expected.get('code') == response.get('code')

