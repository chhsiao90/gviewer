import urwid

from search import SearchWidget
from basic import BasicWidget

""" Summary Widget Related Component

Contents:

* `SummaryItem`: One line of the SummaryList
* `SummaryListWalker`: The urwid Walker to iterate over the data_store*
* `SummaryListWidget`: urwid ListBox to display Summary

"""


class SummaryItem(BasicWidget):
    def __init__(self, message, parent):
        self.message = message
        self.title = parent.displayer.to_summary(message)
        super(SummaryItem, self).__init__(self._make_widget(), parent=parent)

    def _make_widget(self):
        return urwid.AttrMap(
            urwid.Text(self.title), "summary", "summary focus")

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == "enter":
            self.parent.open_detail(self.message)
            return None
        return key


class MessageListener(object):
    def __init__(self):
        self.walkers = []

    def on_message(self, message):
        for walker in self.walkers:
            walker.recv(message)

    def _register(self, walker):
        self.walkers.append(walker)

    def _unregister(self, walker):
        self.walkers.remove(walker)


class SummaryListWalker(urwid.SimpleFocusListWalker):
    def __init__(self, parent, content=None):
        super(SummaryListWalker, self).__init__(content or [])
        self.parent = parent
        self.parent.msg_listener._register(self)

    def recv(self, message):
        self.append(SummaryItem(message, parent=self.parent))


class FilterSummaryListWalker(SummaryListWalker):
    def __init__(self, origin_walker, search):
        parent = origin_walker.parent
        content = [m for m in origin_walker if parent.displayer.match(search, m.message, m.title)]
        super(FilterSummaryListWalker, self).__init__(parent, content=content)
        self.search = search

    def recv(self, message):
        title = self.parent.displayer.to_summary(message)
        if self.parent.displayer.match(self.search, message, title):
            self.append(SummaryItem(message, self.parent))

    def close(self):
        self.parent.msg_listener._unregister(self)


class SummaryListWidget(BasicWidget):
    def __init__(self, walker, **kwargs):
        self.base_walker = walker
        self.current_walker = walker
        self.list_box = urwid.ListBox(walker)
        self.search = SearchWidget(self)
        widget = urwid.Pile([self.list_box, ("pack", self.search)])
        super(SummaryListWidget, self).__init__(widget, **kwargs)

    def filter(self, search):
        new_walker = FilterSummaryListWalker(self.base_walker, search) if search else self.base_walker
        if new_walker is not self.current_walker:
            self._update(new_walker)

    def _update(self, walker):
        if self.current_walker is not self.base_walker:
            self.current_walker.close()

        self.current_walker = walker
        self._w.contents.pop(0)
        self._w.contents.insert(0, (urwid.ListBox(walker), self._w.options()))
        self._w.set_focus(0)

    def keypress(self, size, key):
        if key == "/":
            self._w.set_focus(self.search)
            return None
        if key == "q" and isinstance(self.current_walker, FilterSummaryListWalker):
            self.search.clear()
            self.filter(None)
            return None
        return super(SummaryListWidget, self).keypress(size, key)
