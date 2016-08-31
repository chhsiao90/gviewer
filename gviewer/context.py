from action import Actions


class Context(object):
    """GViewer context

    Attributes:
        store: DataStore implementation instance
        displayer: Displayer implemntation instance
        config: Config instance
        summary_actions: dict for key-action mapping
    """
    def __init__(self, store, displayer, config, summary_actions=None):
        self.store = store
        self.displayer = displayer
        self.config = config
        self.summary_actions = summary_actions or Actions()
