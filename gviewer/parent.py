import sys
import urwid
from summary import SummaryListWidget, SummaryListWalker
from store import MessageListener
from detail import DetailWidget
from error import ErrorWidget


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
        self.config = config
        self.data_store = data_store

        self.displayer = displayer
        self.detail_displayers = displayer.get_detail_displayers()
        self.detail_names = [k for k, _ in self.detail_displayers]

        self.msg_listener = MessageListener(self.data_store)

        walker = SummaryListWalker(self)
        self.summary = SummaryListWidget(walker, self)

        header_widget = urwid.AttrMap(urwid.Text(config.header), "header")
        footer_widget = Footer(config.keys)

        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header_widget,
            footer=footer_widget)

    def open_detail(self, message, index):
        try:
            widget = DetailWidget(message, index, self)
            self.set_body(widget)
        except:
            self.on_error(sys.exc_info())

    def to_summary(self):
        self.set_body(self.summary)

    def filter(self, search):
        self.summary.filter(search)

    def clear_search(self):
        self.summary.clear_search()

    def on_error(self, exc_info):
        widget = ErrorWidget(self, exc_info)
        self.set_body(widget)

    def keypress(self, size, key):
        if key in ("q", "Q"):
            if self.get_body() is not self.summary:
                self.to_summary()
                return None
        return super(ParentFrame, self).keypress(size, key)


class Footer(urwid.WidgetWrap):
    def __init__(self, keys):
        text = "; ".join(
            ["{0}: {1}".format(k, v) for k, v in keys.iteritems()])
        widget = urwid.Text(text)
        widget = urwid.AttrMap(widget, "footer")
        super(Footer, self).__init__(widget)
