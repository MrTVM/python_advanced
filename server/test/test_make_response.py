from datetime import datetime
from protocol import (make_response)


def test_make_response():
    action_name = 'echo'
    user = 'user'
    data = 'some data'
    code = 200

    request = {
        'action': action_name,
        'user': user,
        'time': datetime.now().timestamp(),
        'data': data
    }

    expected = {
        'action': action_name,
        'user': user,
        'time': None,
        'data': data,
        'code': 200
    }

    response = make_response(request, code)

    assert expected.get('code') == response.get('code')
    assert expected.get('user') == response.get('user')

