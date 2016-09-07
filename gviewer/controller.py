class Controller(object):
    """Controller provide UI interaction API

    Attributes:
        parent: ParentFrame instance
    """
    def __init__(self, parent):
        self.parent = parent

    def open_view(self, widget, push_prev=True):
        """Open view

        Args:
            widget: a urwid Widget implementation
            push_prev: bool defined that should push previous widget
                       into history
        """
        self.parent.open_view(widget, push_prev=push_prev)

    def open_view_by_context(self, context):
        """Open view by defined context

        Args:
            context: DisplayerContext
        """
        self.parent.open_view_by_context(context)

    def notify(self, message):
        """Notify a message"""
        self.parent.notify(message)

    def open_edit(self, widget):
        """Open edit box in footer"""
        self.parent.open_edit(widget)

    def close_edit(self):
        """Close edit box"""
        self.parent.close_edit()

    def open_error(self):
        """Open error stacktrace view"""
        self.parent.open_error()

    def back(self):
        """Back to previous view"""
        self.parent.back()

    def _update_info(self, widget, info):
        self.parent.update_info(widget, info)

    def _focus_body(self):
        self.parent.focus_position = "body"

    def _run_before_keypress(self):
        self.parent.run_before_keypress()
