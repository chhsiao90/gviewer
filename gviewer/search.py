import urwid
from basic import BasicWidget


class SearchWidget(BasicWidget):
    def __init__(self, parent):
        super(SearchWidget, self).__init__(
            parent=parent, widget=urwid.Edit())

    def clear(self):
        self._w.set_edit_text("")

    def keypress(self, size, key):
        if key == "enter":
            self.parent.filter(self._w.edit_text)
            return None
        if key == "esc":
            self.parent.filter(None)
            return None
        return self.default_keypress(size, key)
