import urwid
from summary import SummaryListWidget, SummaryListWalker
from detail import DetailWidget


""" Parent Frame to control the which widget to display """


class ParentFrame(urwid.Frame):
    """
    Parent Frame to control the which widget to display
    :param data_store:
    :type data_store: BaseDataStore Implementation

    :param displayer:
    :type displayer: BaseDisplayer implmementation

    :param header: header title
    :type header: str
    """
    def __init__(self, data_store, displayer, config):
        header_widget = urwid.AttrMap(urwid.Text(config.header), "header")
        self.config = config
        self.data_store = data_store
        self.displayer = displayer
        self.walker = SummaryListWalker(parent=self)
        self.summary = SummaryListWidget(self.walker, parent=self)
        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header_widget)

    def open_detail(self, message):
        self.set_body(DetailWidget(message, parent=self))

    def close_detail(self):
        self.set_body(self.summary)

    def keypress(self, size, key):
        if key in ("q", "Q"):
            if isinstance(self.get_body(), DetailWidget):
                self.close_detail()
                return None
        return super(ParentFrame, self).keypress(size, key)
