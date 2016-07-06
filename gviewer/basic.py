import urwid


class BasicWidget(urwid.WidgetWrap):
    def __init__(self, parent=None, widget=None):
        super(BasicWidget, self).__init__(widget or "")
        self.parent = parent

    def display(self, widget):
        self._w = widget

    def keypress(self, size, key):
        if self.parent and key in self.parent.config.keys:
            return super(BasicWidget, self) \
                .keypress(size, self.parent.config.keys[key])
        return super(BasicWidget, self).keypress(size, key)
