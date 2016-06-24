import urwid
from summary import SummaryList, SummaryListWalker
from detail import Detail


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
    def __init__(self, data_store, displayer, header):
        header_widget = urwid.AttrMap(urwid.Text(header), "header")
        self.data_store = data_store
        self.displayer = displayer
        self.walker = SummaryListWalker(self, data_store, displayer)
        self.summary = SummaryList(self.walker)
        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header_widget)

    def open_detail(self, message):
        self.set_body(Detail(self.displayer, message))

    def close_detail(self):
        self.set_body(self.summary)

    def keypress(self, size, key):
        if key in ("q", "Q"):
            if isinstance(self.get_body(), Detail):
                self.close_detail()
                return None
        return super(ParentFrame, self).keypress(size, key)
