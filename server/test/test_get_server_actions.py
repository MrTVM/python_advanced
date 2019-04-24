from datetime import datetime
from actions import (get_server_actions)


def test_get_server_actions():
    action_name = 'echo'

    expected = (
        {'action': action_name, 'controller': 'get_echo'},
    )

    response = get_server_actions()

    assert type(expected) == type(response)
    assert expected[0].get('action') == response[0].get('action')

