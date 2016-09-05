class Controller(object):
    def __init__(self, parent, context):
        self.parent = parent
        self.context = context

    def open_view(self, widget, push_prev=True):
        self.parent.open_view(widget, push_prev)

    def notify(self, message):
        self.parent.notify(message)

    def open_error(self):
        self.parent.open_error()

    def back(self):
        self.parent.back()

    def _run_before_keypress(self):
        self.parent.run_before_keypress()
