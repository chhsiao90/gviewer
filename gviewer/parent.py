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

        self.main = SummaryListWidget(
            context.main_context, controller=self.controller,
            context=self.context)
        self.others = {
            ctx: SummaryListWidget(ctx, controller=self.controller,
                                   context=self.context) for ctx in context.other_contexts}

        header = urwid.Text(context.config.header)
        header = urwid.AttrMap(header, "header")
        self.footer = Footer(controller=self.controller)

        self.histories = []

        super(ParentFrame, self).__init__(
            body=self.main,
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
            self.histories.append(curr_widget)

        self.set_body(widget)
        widget.update_info()

    def open_view_by_context(self, context):
        """Open view by defined context

        Args:
            context: DisplayerContext
        """
        try:
            self.open_view(self.others[context])
        except:
            self.open_error()

    def back(self):
        """Back to previous view"""
        if self.histories:
            self.open_view(self.histories.pop(), push_prev=False)
        else:
            raise urwid.ExitMainLoop()

    def open_error(self):
        """Open ErrorWidget"""
        widget = ErrorWidget(controller=self.controller, context=self.context)
        self.open_view(widget, True)

    def notify(self, message):
        """Notify message"""
        self.footer.notify(message)

    def open_edit(self, widget):
        self.footer.open_edit(widget)
        self.focus_position = "footer"

    def close_edit(self):
        self.footer.close_edit()

    def update_info(self, widget, info):
        if widget is self.contents["body"][0]:
            self.footer.update_info(info)

    def run_before_keypress(self):
        """Some UI cleanup actions to make sure GViewer in a consist state"""
        self.footer.clear_notify()


class Footer(BasicWidget):
    """Footer widget for ParentFrame"""
    def __init__(self, notification=None, helper=None, **kwargs):
        self.notification = notification or Notification(**kwargs)
        self.helper = helper or Helper()
        widgets = [
            ("pack", self.helper),
            ("pack", self.notification)
        ]
        widget = urwid.Pile(widgets)
        super(Footer, self).__init__(
            widget=widget, **kwargs)

    def notify(self, message):
        """Notify message"""
        self.notification.notify(message)

    def clear_notify(self):
        self.notification.clear()

    def open_edit(self, widget):
        self.notification.open_edit(widget)

    def close_edit(self):
        self.notification.close_edit()

    def update_info(self, info):
        self.helper.update_info(info)


class Helper(BasicWidget):
    """Helper widget contains basic help words"""
    def __init__(self, info_widget=None):
        self.info_widget = info_widget or urwid.Text("")
        widget = urwid.Text("?:help")
        widget = urwid.Padding(
            widget, "right", "pack")
        widget = urwid.Columns([self.info_widget, widget])
        super(Helper, self).__init__(
            widget=widget, attr_map="footer helper")

    def update_info(self, info):
        self.info_widget.set_text(info)


class Notification(BasicWidget):
    """Notification widget"""
    EMPTY_WIDGET = urwid.Text("")

    def __init__(self, **kwargs):
        self._edit_widget = None
        super(Notification, self).__init__(
            widget=self.EMPTY_WIDGET,
            attr_map="footer info", **kwargs)

    def is_editing(self):
        return bool(self._edit_widget)

    def selectable(self):
        return True

    def notify(self, message):
        """Notify message"""
        self.display(urwid.Text(message))

    def clear(self):
        """Clear message"""
        self.display(self._edit_widget or self.EMPTY_WIDGET)

    def open_edit(self, widget):
        self._edit_widget = widget
        self.display(widget)

    def close_edit(self):
        self._edit_widget = None
        self.display(self.EMPTY_WIDGET)
