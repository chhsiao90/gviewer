import urwid
from urwid.util import decompose_tagmarkup


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

    def default_keypress(self, size, key):
        return super(BasicWidget, self).keypress(size, key)


class FocusableText(urwid.WidgetWrap):
    def __init__(self, text_markup):
        widget = urwid.Text(text_markup)
        super(FocusableText, self).__init__(widget)
        self.text_markup = text_markup

    def render(self, size, focus=False):
        if focus:
            plain_text = self.get_plain_text()
            self._w = urwid.Text(plain_text)
        else:
            self._w = urwid.Text(self.text_markup)
        return super(FocusableText, self).render(size, focus)

    def get_plain_text(self):
        if isinstance(self.text_markup, str) or \
           isinstance(self.text_markup, unicode):
            return self.text_markup
        text, _ = decompose_tagmarkup(self.text_markup)
        return text

    def selectable(self):
        return True
