import urwid
import time

from gviewer.basic import BasicWidget, SearchWidget


class ViewWidget(BasicWidget):
    """ Display content for message

    Attributes:
        message: message generate by DataStore
        index: view's index
        parent: ParentFrame instance
    """
    def __init__(self, message, index, parent):
        super(ViewWidget, self).__init__(parent)
        self.index = index
        self.message = message

        self.search_widget = SearchWidget(self._search, self._clear_search)

        _, view_callable = self.parent.views[index]
        self.view = view_callable(self.message)

        self.content_widget = self.view.to_widget(self.parent, self.message)
        self.body = urwid.Pile([self.content_widget])

        if len(self.parent.view_names) > 1:
            header = Tabs(self.parent.view_names, self.index)
        else:
            header = None

        widget = urwid.Frame(self.body, header=header)
        self.display(widget)

    def _next_view(self):
        if len(self.parent.view_names) == 1:
            return

        if len(self.parent.view_names) > self.index + 1:
            next_index = self.index + 1
        else:
            next_index = 0
        self.parent.display_view(self.message, next_index)

    def _prev_view(self):
        if len(self.parent.view_names) == 1:
            return

        next_index = len(self.parent.view_names) - 1 if self.index == 0 else self.index - 1
        self.parent.display_view(self.message, next_index)

    def _open_search(self):
        self.search_widget.clear()
        self.content_widget.clear_prev_search()
        if len(self.body.contents) == 1:
            self.body.contents.append((
                self.search_widget,
                self.body.options(height_type="pack"))
            )
        self.body.focus_position = 1

    def _close_search(self):
        if len(self.body.contents) == 2:
            del self.body.contents[1]

    def _search(self, keyword):
        self.content_widget.search_next(keyword)
        self._close_search()

    def _clear_search(self):
        self._close_search()

    def is_editing(self):
        return self.body.focus is self.search_widget

    def _export(self):
        file_name = "export-%13d" % (time.time() * 1000)
        with open(file_name, "w") as f:
            f.write(self.view.text())
        self.parent.notify("Export to file {0}".format(file_name))

    def keypress(self, size, key):
        if self.is_editing():
            return super(ViewWidget, self).keypress(size, key)
        if key == "q":
            self.parent.open_summary()
            return None
        if key == "tab":
            self._next_view()
            return None
        if key == "shift tab":
            self._prev_view()
            return None
        if key == "/":
            self._open_search()
            return None
        if key == "n":
            if self.search_widget.get_keyword():
                self.content_widget.search_next(
                    self.search_widget.get_keyword()
                )
            return None
        if key == "N":
            if self.search_widget.get_keyword():
                self.content_widget.search_prev(
                    self.search_widget.get_keyword()
                )
            return None
        if key == "e":
            self._export()
            return None
        return super(ViewWidget, self).keypress(size, key)  # pragma: no cover


class Tabs(BasicWidget):
    """Tab to display title for each view"""
    def __init__(self, view_names, index):
        widget = self._make_widget(view_names, index)
        super(Tabs, self).__init__(widget=widget)

    def _make_widget(self, view_names, index):
        def make_tab(curr_index):
            name = view_names[curr_index]
            if curr_index == index:
                return urwid.AttrMap(urwid.Text(name), "tabs focus")
            return urwid.AttrMap(urwid.Text(name), "tabs")
        widgets = map(make_tab, range(0, len(view_names)))
        return urwid.Columns(widgets)
