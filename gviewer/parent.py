import urwid

from .basic_widget import BasicWidget
from .controller import Controller
from .view.summary import SummaryListWidget
from .view.error import ErrorWidget


class ParentFrame(urwid.Frame):
    """ Parent Frame to control the which widget to display

    Attributes:
        context: Context
    """
    def __init__(self, context):
        self.context = context
        self.controller = Controller(self)

        self.summary = SummaryListWidget(
            context.main_displayer_context, controller=self.controller,
            context=self.context)

        header = urwid.Text(context.config.header)
        header = urwid.AttrMap(header, "header")
        self.footer = Footer(controller=self.controller)

        self.prev_views = []

        super(ParentFrame, self).__init__(
            body=self.summary,
            header=header,
            footer=self.footer)

    def open_view(self, widget, push_prev=True):
        """Open widget

        Args:
            widget: Widget
            push_prev: Boolean to record previous view
        """
        curr_widget = self.contents["body"][0]

        if widget is curr_widget:
            return

        if push_prev:
            self.prev_views.append(curr_widget)

        self.set_body(widget)

    def back(self):
        """Back to previous view"""
        self.set_body(self.prev_views.pop())

    def open_error(self):
        """Open ErrorWidget"""
        widget = ErrorWidget(controller=self.controller, context=self.context)
        self.open_view(widget, True)

    def notify(self, message):
        """Notify message"""
        self.footer.notify(message)

    def run_before_keypress(self):
        """Some UI cleanup actions to make sure GViewer in a consist state"""
        self.footer.notify("")


class Footer(BasicWidget):
    """Footer widget for ParentFrame"""
    def __init__(self, **kwargs):
        self.notification = Notification(**kwargs)
        widgets = [
            ("pack", Helper()),
            ("pack", self.notification)
        ]
        widget = urwid.Pile(widgets)
        super(Footer, self).__init__(
            widget=widget, **kwargs)

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
    """Notification widget"""
    def __init__(self, **kwargs):
        self.message = ""
        super(Notification, self).__init__(
            widget=urwid.Text(""),
            attr_map="footer info", **kwargs)

    def notify(self, message):
        """Notify message"""
        if self.message != message:
            self.message = message
            self.display(urwid.Text(message))
