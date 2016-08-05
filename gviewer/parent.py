import sys
import urwid
from summary import SummaryListWidget, SummaryListWalker
from store import MessageListener
from view import ViewWidget
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
        self.views = displayer.get_views()
        self.view_names = [k for k, _ in self.views]

        self.msg_listener = MessageListener(self.data_store)

        walker = SummaryListWalker(self)
        self.summary = SummaryListWidget(walker, self)

        header_widget = urwid.AttrMap(urwid.Text(config.header), "header")
        footer_widget = Footer(config.keys)

        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header_widget,
            footer=footer_widget)

    def display_view(self, message, index):
        try:
            widget = ViewWidget(message, index, self)
            self.set_body(widget)
        except:
            self.open_error(sys.exc_info())

    def open_summary(self):
        self.set_body(self.summary)

    def open_error(self, exc_info):
        widget = ErrorWidget(self, exc_info)
        self.set_body(widget)


class Footer(urwid.WidgetWrap):
    def __init__(self, keys):
        text = "; ".join(
            ["{0}: {1}".format(k, v) for k, v in keys.iteritems()])
        widget = urwid.Text(text)
        widget = urwid.AttrMap(widget, "footer")
        super(Footer, self).__init__(widget)
