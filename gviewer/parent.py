import urwid
from summary import SummaryList, SummaryListWalker
from detail import Detail


class ParentFrame(urwid.Frame):
    def __init__(self, data_store, header):
        header_widget = urwid.AttrMap(urwid.Text(header), "header")
        self.data_store = data_store
        self.walker = SummaryListWalker(self, data_store)
        self.summary = SummaryList(self, data_store, self.walker)
        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header_widget)

    def open_detail(self, message):
        self.set_body(Detail(self.data_store, message))

    def close_detail(self):
        self.set_body(self.summary)

    def keypress(self, size, key):
        if key in ("q", "Q"):
            if isinstance(self.get_body(), Detail):
                self.close_detail()
                return None
        return super(ParentFrame, self).keypress(size, key)
