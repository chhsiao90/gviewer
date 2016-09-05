import urwid
import time
from collections import OrderedDict

from ..basic_widget import BasicWidget, SearchWidget
from .helper import (
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


def _verify_keys(actions):
    for key, _, _ in actions:
        if key in _ADVANCED_KEYS:
            raise ValueError("key '{0}' had defined by GViewer for {1}".format(key, _ADVANCED_KEYS[key]))


class DetailWidget(BasicWidget):
    """ Display content for message

    Attributes:
        message: message generate by DataStore
        displayer_context: DisplayerContext instance
        index: view's index
    """
    def __init__(self, message, displayer_context, index=0, **kwargs):
        super(DetailWidget, self).__init__(**kwargs)
        self.index = index
        self.message = message
        self.displayer_context = displayer_context

        self.views = self.displayer_context.displayer.get_views()
        self.view = self.views[index][1].__call__(self.message)

        self.content_widget = self.view.widget(
            self.message, **kwargs)

        _verify_keys(self.view.actions)
        self.search_widget = SearchWidget(self._search, self._clear_search)
        self.help_widget = HelpWidget(
            HelpContent(
                [HelpCategory("Basic", self.context.config.keys),
                 HelpCategory("Advanced", _ADVANCED_KEYS),
                 make_category_with_actions("Custom", self.view.actions)]),
            **kwargs
        )

        self.body = urwid.Pile([self.content_widget])

        if len(self.views) > 1:
            header = Tabs([k for k, _ in self.views], self.index)
        else:
            header = None

        widget = urwid.Frame(self.body, header=header)
        self.display(widget)

    def _open(self, index):
        self.controller.open_view(DetailWidget(
            self.message, self.displayer_context, index=index,
            controller=self.controller, context=self.context),
            push_prev=False)

    def _next_view(self):
        if len(self.views) == 1:
            return

        if len(self.views) > self.index + 1:
            next_index = self.index + 1
        else:
            next_index = 0
        self._open(next_index)

    def _prev_view(self):
        if len(self.views) == 1:
            return

        next_index = len(self.views) - 1 if self.index == 0 else self.index - 1
        self._open(next_index)

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
            f.write(str(self.view).encode("utf8"))
        self.controller.notify("Export to file {0}".format(file_name))

    def keypress(self, size, key):
        if self.is_editing():
            return super(DetailWidget, self).keypress(size, key)
        if key == "q":
            self.controller.back()
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
            self.controller.open_view(self.help_widget)
            return None

        return super(DetailWidget, self).keypress(size, key)  # pragma: no cover


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
