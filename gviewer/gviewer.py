import urwid
from parent import ParentFrame
from styles import default


"""A General Purpose tui Viewer library that based on urwid """


class GViewer(object):
    """
    """
    def __init__(self, data_store, displayer, palette=default,
                 header="GViewer", **kwargs):
        self.view = ParentFrame(data_store, displayer, header)
        self.loop = urwid.MainLoop(
            self.view, palette, **kwargs)
        self.data_store = data_store

    def start(self):
        """ Use this method to start tui
        """
        self.data_store.set_up()
        self.loop.run()
