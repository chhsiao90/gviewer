import urwid
from parent import ParentFrame
from config import Config
from styles import default


"""A General Purpose tui Viewer library that based on urwid """


class GViewer(object):
    """
    General Viewer Main Class
    :param data_store:
    :type data_store: BaseDataStore Implementation

    :param displayer:
    :type displayer: BaseDisplayer implmementation

    :param palette:
    :type palette: iterable for patette entries

    :param config: GViewer general config
    :type config: Config

    :param **kwargs: other urwid.MainLoop supported parameters
    """
    def __init__(self, data_store, displayer, config=None, template=default, palette=None, **kwargs):
        self.config = config or Config()
        self.view = ParentFrame(data_store, displayer, self.config)

        if "unhandled_input" not in kwargs:
            kwargs["unhandled_input"] = self.default_unhandled_input

        palette = palette or []
        self.loop = urwid.MainLoop(
            self.view, template + palette, **kwargs)
        self.data_store = data_store

    def default_unhandled_input(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()

    def start(self):
        """ Use this method to start tui
        """
        self.data_store.set_up()
        self.loop.run()
