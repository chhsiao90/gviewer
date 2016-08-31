import urwid
import time
from collections import OrderedDict

from gviewer.basic import BasicWidget, SearchWidget
from gviewer.helper import (
    HelpWidget, HelpContent, HelpCategory,
    make_category_with_actions)


_ADVANCED_KEYS = OrderedDict([
    ("/", "search"),
    ("tab", "next view"),
    ("shift+tab", "prev view"),
    ("n", "search next result"),
    ("N", "search prev result"),
    ("e", "export content to file"),
    ("q", "quit")
])


class ViewWidget(BasicWidget):
    """ Display content for message

    Attributes:
        message: message generate by DataStore
        index: view's index
        parent: ParentFrame instance
    """
    def __init__(self, message, index, parent, context):
        super(ViewWidget, self).__init__(
            parent=parent, context=context)
        self.index = index
        self.message = message

        _, view_callable = self.parent.views[index]
        self.view = view_callable(self.message)

        self.content_widget = self.view.to_widget(self.parent, self.context, self.message)

        self.search_widget = SearchWidget(self._search, self._clear_search)
        self.help_widget = HelpWidget(
            parent,
            context,
            HelpContent(
                [HelpCategory("Basic", self.context.config.keys),
                 HelpCategory("Advanced", _ADVANCED_KEYS),
                 make_category_with_actions("Custom", self.view.actions)])
        )

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
        self.parent.display_view(self.message, next_index, push_prev=False)

    def _prev_view(self):
        if len(self.parent.view_names) == 1:
            return

        next_index = len(self.parent.view_names) - 1 if self.index == 0 else self.index - 1
        self.parent.display_view(self.message, next_index, push_prev=False)

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

    def _export(self):  # pragma: no cover
        file_name = "export-%13d" % (time.time() * 1000)
        with open(file_name, "w") as f:
            f.write(self.view.text().encode("utf8"))
        self.parent.notify("Export to file {0}".format(file_name))

    def keypress(self, size, key):
        if self.is_editing():
            return super(ViewWidget, self).keypress(size, key)
        if key == "q":
            self.parent.back()
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
        if key == "e":  # pragma: no cover
            self._export()
            return None
        if key == "?":  # pragma: no cover
            self.parent.open(self.help_widget)
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
