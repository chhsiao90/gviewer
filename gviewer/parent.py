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
        context: Context
    """
    def __init__(self, context):
        self._context = context

        self.views = context.displayer.get_views()
        self.view_names = [k for k, _ in self.views]

        self.msg_listener = MessageListener(context.store)

        walker = SummaryListWalker(self, context)
        self._summary = SummaryListWidget(walker, self, context)

        header = urwid.Text(context.config.header)
        header = urwid.AttrMap(header, "header")
        self._footer = Footer(self)

        self._prev_views = []

        super(ParentFrame, self).__init__(
            body=self._summary,
            header=header,
            footer=self._footer)

    def display_view(self, message, index, push_prev=True):
        """ Display view for message

        Args:
            message: Message generate by DataStore
            index: int represent which view to display
        """
        try:
            widget = ViewWidget(message, index, self, self._context)
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
        widget = ErrorWidget(self, self._context, exc_info)
        self.open(widget, True)

    def notify(self, message):
        """Notify message"""
        self._footer.notify(message)

    def run_before_keypress(self):
        self._footer.notify("")


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
        self.message = ""
        super(Notification, self).__init__(
            parent=parent,
            widget=urwid.Text(""),
            attr_map="footer info")

    def notify(self, message):
        """Notify message"""
        if self.message != message:
            self.message = message
            self.display(urwid.Text(message))
