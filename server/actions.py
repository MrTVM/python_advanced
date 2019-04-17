from functools import reduce
from setting import INSTALLED_MODULES


def get_server_actions():
    return reduce(
        lambda value, item: value + getattr(item, 'action_names', tuple()),
        reduce(
            lambda value, item: value + (getattr(item, 'actions', tuple()),),
            reduce(
                lambda value, item: value + (__import__(f'{item}.actions'),),
                INSTALLED_MODULES,
                tuple(),
            ),
            tuple(),
        ),
        tuple(),
    )


def resolve(action, actions=None):
    return reduce(
        lambda value, item: item.get('controller') if item.get('action') == action else None,
        actions or get_server_actions(),
    )

