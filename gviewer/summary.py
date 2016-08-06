import sys
import urwid

from basic import BasicWidget, FocusableText, SearchWidget

""" Summary Widget Related Component

Contents:

* `SummaryItemWidget`: One line of the SummaryList
* `SummaryListWalker`: The urwid Walker to iterate over the data_store
* `FilterSummaryListWalker`: The urwid Walker to iterate over the data_store with filter
* `SummaryListWidget`: urwid ListBox to display Summary

"""


class SummaryItemWidget(BasicWidget):
    def __init__(self, parent, message, summary):
        super(SummaryItemWidget, self).__init__(parent)

        self.message = message
        widget = FocusableText(summary)
        self.title = widget.get_plain_text()
        widget = urwid.AttrMap(widget, "summary", "summary focus")
        self.display(widget)

    def keypress(self, size, key):
        if key == "enter":
            self.parent.display_view(self.message, 0)
            return None
        return key


class SummaryListWalker(urwid.SimpleFocusListWalker):
    def __init__(self, parent, content=None):
        super(SummaryListWalker, self).__init__(content or [])
        self.parent = parent
        self.parent.msg_listener.register(self)

    def recv(self, message):
        try:
            summary = self.parent.displayer.summary(message)
            self.append(SummaryItemWidget(self.parent, message, summary))
        except:
            self.parent.open_error(sys.exc_info())


class FilterSummaryListWalker(SummaryListWalker):
    def __init__(self, origin_walker, search):
        parent = origin_walker.parent
        content = [m for m in origin_walker if parent.displayer.match(search, m.message, m.title)]
        super(FilterSummaryListWalker, self).__init__(parent, content=content)
        self.search = search

    def recv(self, message):
        try:
            summary = self.parent.displayer.summary(message)
            if self.parent.displayer.match(self.search, message, summary):
                self.append(SummaryItemWidget(self.parent, message, summary))
        except:
            self.parent.open_error(sys.exc_info())

    def close(self):
        self.parent.msg_listener.unregister(self)


class SummaryListWidget(BasicWidget):
    def __init__(self, walker, parent):
        super(SummaryListWidget, self).__init__(parent)
        self.base_walker = walker
        self.current_walker = walker
        self.list_box = urwid.ListBox(walker)
        self.search_widget = SearchWidget(self.filter, self.clear_search)

        widget_list = [self.list_box]
        widget = urwid.Pile(widget_list)
        self.display(widget)

    def filter(self, keyword):
        new_walker = FilterSummaryListWalker(self.base_walker, keyword) if keyword else self.base_walker
        if new_walker is not self.current_walker:
            self._update(new_walker)

        self.close_search()
        self._w.set_focus(0)

    def _update(self, walker):
        if self.current_walker is not self.base_walker:
            self.current_walker.close()

        self.current_walker = walker
        self._w.contents.pop(0)
        self._w.contents.insert(0, (urwid.ListBox(walker), self._w.options()))

    def open_search(self):
        if len(self._w.contents) == 1:
            self._w.contents.append((
                self.search_widget,
                self._w.options(height_type="pack"))
            )
        self._w.set_focus(self.search_widget)

    def close_search(self):
        if len(self._w.contents) == 2:
            del self._w.contents[1]

    def clear_search(self):
        self.search_widget.clear()
        self.filter(None)

    def is_editing(self):
        return self._w.get_focus() is self.search_widget

    def keypress(self, size, key):
        if self.is_editing():
            return super(SummaryListWidget, self).keypress(size, key)
        if key == "/":
            self.open_search()
            return None
        if key == "q" and isinstance(self.current_walker, FilterSummaryListWalker):
            self.clear_search()
            return None

        return super(SummaryListWidget, self).keypress(size, key)
