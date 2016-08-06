import urwid
from urwid.util import decompose_tagmarkup


class BasicWidget(urwid.WidgetWrap):
    def __init__(self, parent=None, widget=None):
        super(BasicWidget, self).__init__(widget or "")
        self.parent = parent

    def display(self, widget):
        self._w = widget

    def keypress(self, size, key):
        if not self.is_editing() and self.parent and key in self.parent.config.keys:
            return super(BasicWidget, self) \
                .keypress(size, self.parent.config.keys[key])
        return super(BasicWidget, self).keypress(size, key)

    def is_editing(self):
        return False


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


class SearchWidget(urwid.WidgetWrap):
    def __init__(self, search_func, clear_func):
        super(SearchWidget, self).__init__(urwid.Edit())
        self.search_func = search_func
        self.clear_func = clear_func

    def clear(self):
        self._w.set_edit_text("")

    def get_keyword(self):
        return self._w.edit_text

    def keypress(self, size, key):
        if key == "enter":
            self.search_func(self._w.edit_text)
            return None
        if key == "esc":
            self.clear_func()
            return None
        super(SearchWidget, self).keypress(size, key)


class SearchableText(urwid.WidgetWrap):
    def __init__(self, plain_text):
        plain_text = plain_text or ""
        if not isinstance(plain_text, (str, unicode)):
            plain_text = decompose_tagmarkup(plain_text)
        plain_text = plain_text.decode("utf8") if isinstance(plain_text, str) else plain_text
        widget = urwid.Text(plain_text)
        super(SearchableText, self).__init__(widget)
        self.plain_text = plain_text
        self.prev_index = (0, len(plain_text))

    def search_next(self, keyword):
        prev_index = self.prev_index[0]
        if isinstance(keyword, str):
            keyword = keyword.decode("utf8")
        if keyword in self.plain_text[prev_index:]:
            start_index = self.plain_text[prev_index:].index(keyword) + prev_index
            end_index = start_index + len(keyword)
            self._w = urwid.Text([
                self.plain_text[:start_index],
                ("match", keyword),
                self.plain_text[end_index:]
            ])

            self.prev_index = (end_index, start_index)
            return True
        else:
            self.clear()
            return False

    def search_prev(self, keyword):
        prev_index = self.prev_index[1]
        if keyword in self.plain_text[:prev_index]:
            start_index = self.plain_text[:prev_index].rindex(keyword)
            end_index = start_index + len(keyword)
            self._w = urwid.Text([
                self.plain_text[:start_index],
                ("match", keyword),
                self.plain_text[end_index:]
            ])

            self.prev_index = (end_index, start_index)
            return True
        else:
            self.clear()
            return False

    def clear(self):
        self.prev_index = (0, len(self.plain_text))
        self._w = urwid.Text(self.plain_text)
