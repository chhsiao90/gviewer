import urwid


class BasicWidget(urwid.WidgetWrap):
    def __init__(self, parent, widget):
        self.parent = parent
        super(BasicWidget, self).__init__(widget)

    def keypress(self, size, key):
        if key in self.parent.config.keys:
            return super(BasicWidget, self).keypress(size, self.parent.config.keys[key])
        return super(BasicWidget, self).keypress(size, key)
