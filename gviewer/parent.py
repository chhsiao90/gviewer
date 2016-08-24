import sys
import urwid
from summary import SummaryListWidget, SummaryListWalker
from basic import BasicWidget
from store import MessageListener
from view import ViewWidget
from error import ErrorWidget


class ParentFrame(urwid.Frame):
    """ Parent Frame to control the which widget to display

    Attributes:
        data_store: BaseDataStore implementation instance
        displayer: BaseDisplayer implmementation
        config: Config instance
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

        header = urwid.AttrMap(urwid.Text(config.header), "header")
        self.footer = Footer(self)

        self._prev_views = []

        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header,
            footer=self.footer)

    def display_view(self, message, index, push_prev=True):
        """ Display view for message

        Args:
            message: Message generate by DataStore
            index: int represent which view to display
        """
        try:
            widget = ViewWidget(message, index, self)
            self.open(widget, push_prev)
        except:  # pragma: no cover
            self.open_error(sys.exc_info())

    def open(self, widget, push_prev=True):
        """Open widget

        Args:
            widget: Widget
            push_prev: Boolean to record previous view
        """
        curr_widget = self.contents["body"][0]

        if widget is curr_widget:
            return

        if push_prev:
            self._prev_views.append(curr_widget)

        self.set_body(widget)

    def back(self):
        """Back to previous view"""
        self.set_body(self._prev_views.pop())

    def open_error(self, exc_info):
        """ Open ErrorWidget

        Args:
            exc_info: sys.exc_info()
        """
        widget = ErrorWidget(self, exc_info)
        self.open(widget, True)

    def notify(self, message):
        """Notify message"""
        self.footer.notify(message)
        self.focus_position = "footer"
        self.footer._w.focus_position = 1

    def exit_notify(self):
        """Unfocus notification widget"""
        self.focus_position = "body"


class Footer(BasicWidget):
    """Footer widget for ParentFrame"""
    def __init__(self, parent):
        self.notification = Notification(parent)
        widgets = [
            ("pack", Helper()),
            ("pack", self.notification)
        ]
        widget = urwid.Pile(widgets)
        super(Footer, self).__init__(
            parent=parent,
            widget=widget)

    def notify(self, message):
        """Notify message"""
        self.notification.notify(message)


class Helper(BasicWidget):
    """Helper widget contains basic help words"""
    def __init__(self):
        widget = urwid.Text("?:help")
        widget = urwid.Padding(
            widget, "right", "pack")
        super(Helper, self).__init__(
            widget=widget, attr_map="footer helper")


class Notification(BasicWidget):
    def __init__(self, parent):
        super(Notification, self).__init__(
            parent=parent,
            widget=urwid.Text(""),
            attr_map="footer info")

    def selectable(self):
        return True

    def notify(self, message):
        """Notify message"""
        self.display(urwid.Text(message))

    def keypress(self, size, key):
        self.display(urwid.Text(""))
        self.parent.exit_notify()
        if key == "q":
            return None
        return key
