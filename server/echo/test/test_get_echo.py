from datetime import datetime
from server.echo.controllers import get_echo


def test_get_echo():
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
        'code': 200
    }

    response = get_echo(request)

    assert expected.get('data') == response.get('data')

