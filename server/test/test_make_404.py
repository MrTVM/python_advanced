from datetime import datetime
from protocol import (make_404)


def test_make_404():
    action_name = 'echo'
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
        'code': 404
    }

    response = make_404(request)

    assert expected.get('code') == response.get('code')

