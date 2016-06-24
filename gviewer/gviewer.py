import urwid
from parent import ParentFrame
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

    :param header: header title
    :type header: str

    :param **kwargs: other urwid.MainLoop supported parameters
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
