import urwid
from parent import ParentFrame
from styles import default


class GViewer(object):
    def __init__(self, data_store, palette=default,
                 header="GViewer", **kwargs):
        self.view = ParentFrame(data_store, header)
        self.loop = urwid.MainLoop(
            self.view, palette, **kwargs)
        self.data_store = data_store

    def start(self):
        self.data_store.set_up()
        self.loop.run()
