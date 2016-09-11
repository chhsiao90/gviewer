from collections import OrderedDict


class Action(object):
    """Action defined action

    Attributes:
        desc: description for the action
        function: callable for callback when keypress
    """
    def __init__(self, desc, function):
        self.desc = desc
        self.function = function

    def __call__(self, *args, **kwargs):
        self.function.__call__(*args, **kwargs)


class Actions(object):
    """Actions contains action list

    Attributes:
        actions: dict contains k->Action
    """
    def __init__(self, actions=None):
        actions = actions or []
        if not isinstance(actions, list):  # pragma: no cover
            raise ValueError("Actions cannot accept {0}".format(type(actions)))
        self.actions = OrderedDict([
            (k, Action(d, f)) for (k, d, f) in actions
        ])

    def __contains__(self, key):
        return key in self.actions

    def __getitem__(self, key):
        return self.actions[key]

    def __iter__(self):
        return iter([(k, a.desc, a.function) for k, a in self.actions.items()])
