import urwid


class SearchWidget(urwid.WidgetWrap):
    def __init__(self, summary):
        super(SearchWidget, self).__init__(urwid.Edit())
        self.summary = summary

    def clear(self):
        self._w.set_edit_text("")

    def keypress(self, size, key):
        if key == "enter":
            self.summary.filter(self._w.edit_text)
            return None
        return super(SearchWidget, self).keypress(size, key)
