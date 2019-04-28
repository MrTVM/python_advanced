from functools import reduce
from setting import INSTALLED_MODULES


def get_server_actions():
    return reduce(
        lambda actions, module: actions + getattr(module, 'action_names', tuple()),
        reduce(
            lambda submodules, module: submodules + (getattr(module, 'actions', tuple()),),
            reduce(
                lambda modules, module: modules + (__import__(f'{module}.actions'),),
                INSTALLED_MODULES,
                tuple()
            ),
            tuple()
        ),
        tuple()
    )


def resolve(action, actions=None):
    action_mapper = {
        item.get('action'): item.get('controller')
        for item in actions or get_server_actions()
    }
    return action_mapper[action]

