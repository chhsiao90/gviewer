import urwid

from .parent import ParentFrame
from .config import Config
from .context import Context, DisplayerContext


class GViewer(object):  # pragma: no cover
    """ General viewer main class

    Attributes:
        store: a BaseDataStore implementation instance
        displayer: a BaseDisplayer implementation instance
        config: a Config instance
        others: any other args defined in urwid.MainLoop
    """
    def __init__(self, store, displayer, summary_actions=None, config=None, **kwargs):
        config = config or Config()
        main_displayer_context = DisplayerContext(store, displayer, summary_actions)

        self.context = Context(config, main_displayer_context)
        self.view = ParentFrame(self.context)

        self._default_urwid_options(kwargs)

        self.loop = urwid.MainLoop(
            self.view, **kwargs)

    def _default_urwid_options(self, kwargs):
        """ generate default urwid options

        handle_mouse with False
        unhandled_input with "q", "Q" to exit tui
        palette with predefined template in gviewer

        """
        if "handle_mouse" not in kwargs:
            kwargs["handle_mouse"] = False

        if "unhandled_input" not in kwargs:
            kwargs["unhandled_input"] = self._default_unhandled_input

        if "palette" in kwargs:
            kwargs["palette"] = self.context.config.template + kwargs["palette"]
        else:
            kwargs["palette"] = self.context.config.template

    def _default_unhandled_input(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()

    def start(self):
        """ Start the gviewer tui
        """
        self.context.main_displayer_context.store.setup()
        self.loop.run()
