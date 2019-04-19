from datetime import datetime
from protocol import (validate_request)


def test_validate_request():
    action_name = 'echo'

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
    }

    expected = {
        'positive': True,
        'negative': False
    }

    response = validate_request(request)

    assert expected.get('positive') == response

