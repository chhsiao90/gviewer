from .action import Actions


class Context(object):
    """GViewer context

    Attributes:
        store: DataStore implementation instance
        displayer: Displayer implemntation instance
        config: Config instance
        summary_actions: dict for key-action mapping
    """
    def __init__(self, config, main_displayer_context):
        self.config = config
        self.main_displayer_context = main_displayer_context


class DisplayerContext(object):
    def __init__(self, store, displayer, actions=None):
        self.store = store
        self.displayer = displayer
        self.actions = actions or Actions()
