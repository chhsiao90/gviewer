import urwid
from parent import ParentFrame
from config import Config


class GViewer(object):  # pragma: no cover
    """ General viewer main class

    Attributes:
        data_store: a BaseDataStore implementation instance
        displayer: a BaseDisplayer implementation instance
        config: a Config instance
        others: any other args defined in urwid.MainLoop
    """
    def __init__(self, data_store, displayer, config=None, **kwargs):
        self.config = config or Config()
        self.view = ParentFrame(data_store, displayer, self.config)

        self._default_urwid_options(kwargs)

        self.loop = urwid.MainLoop(
            self.view, **kwargs)
        self.data_store = data_store

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
            kwargs["palette"] = self.config.template + kwargs["palette"]
        else:
            kwargs["palette"] = self.config.template

    def _default_unhandled_input(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()

    def start(self):
        """ Start the gviewer tui
        """
        self.data_store.set_up()
        self.loop.run()
