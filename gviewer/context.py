from .action import Actions


class Context(object):
    """GViewer context

    Attributes:
        config: Config instance
        main_displayer_context: DisplayerContext instance for main view
    """
    def __init__(self, config, main_context, other_contexts=None):
        self.config = config
        self.main_context = main_context
        self.other_contexts = other_contexts or []


class DisplayerContext(object):
    """Context defined for how ui display

    Attributes:
        store: DataStore instance
        displayer: BaseDisplayer implementation instance
        actions: Actions instance
    """
    def __init__(self, store, displayer, actions=None):
        self.store = store
        self.displayer = displayer
        self.actions = actions or Actions()
