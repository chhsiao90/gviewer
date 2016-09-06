import urwid
from collections import OrderedDict

from ..basic_widget import BasicWidget, FocusableText, SearchWidget
from .helper import (
    HelpWidget, HelpContent, HelpCategory,
    make_category_with_actions)
from .detail import DetailWidget


_ADVANCED_KEYS = OrderedDict([
    ("/", "search"),
    ("g", "top"),
    ("G", "bottom"),
    ("x", "clear current item"),
    ("X", "clear all items"),
    ("q", "quit")
])


def _verify_keys(actions):
    for key, _, _ in actions:
        if key in _ADVANCED_KEYS:
            raise ValueError("key '{0}' had defined by GViewer for {1}".format(key, _ADVANCED_KEYS[key]))


class SummaryItemWidget(BasicWidget):
    """ Summary item widget

    Summary item widget that display summary and defined action to open other view

    Attributes:
        message: Original message genrate by BaseDataStore
        summary: Format message by displayer
        displayer_context: DisplayerContext instance
    """
    def __init__(self, message, title, displayer_context, **kwargs):
        super(SummaryItemWidget, self).__init__(
            widget=self._widget(title),
            **kwargs)

        self.displayer_context = displayer_context
        self.message = message

    def _widget(self, title):
        return FocusableText(title, attr_map="summary", focus_map="summary focus")

    def get_title_as_plain_text(self):
        """ Get title in plain text

        Returns:
            title in plain text
        """
        return self._w.get_plain_text()

    def set_title(self, title):
        self.display(self._widget(title))

    def keypress(self, size, key):
        if key == "enter":
            self.controller.open_view(DetailWidget(
                self.message, self.displayer_context, controller=self.controller,
                context=self.context))
            return None
        if key in self.displayer_context.actions:
            try:
                self.displayer_context.actions[key].__call__(
                    self.controller, self.message, self)
            except:  # pragma: no cover
                self.controller.open_error()
            return None

        return super(SummaryItemWidget, self).keypress(size, key)  # pragma: no cover


class SummaryListWalker(urwid.SimpleFocusListWalker):
    """ Summary item widgets wrapper

    Contains the SummaryItemWidget,
    and used to receive message from data store

    Attributes:
        content: list of SummaryItemWidget
        displayer_context: DisplayerContext instance
    """
    def __init__(self, content=None, displayer_context=None,
                 base_walker=None, controller=None, context=None,
                 on_receive=None):
        super(SummaryListWalker, self).__init__(content or [])
        self.controller = controller or base_walker.controller
        self.context = context or base_walker.context
        self.displayer_context = displayer_context or base_walker.displayer_context
        self.on_receive = on_receive or base_walker.on_receive
        self.base_walker = base_walker
        self.displayer_context.store.register(self)

    def recv(self, message):
        """ Action when received message from data store

        Will transform message into summary,
        and generate a SummaryItemWidget into its content
        """
        try:
            self.append(self._create_widget(message))
        except:
            self.controller.open_error()
        else:
            self.on_receive()

    def _create_widget(self, message):
            summary = self.displayer_context.displayer.summary(message)
            return SummaryItemWidget(
                message, summary, self.displayer_context, controller=self.controller, context=self.context)


class FilterSummaryListWalker(SummaryListWalker):
    """ Summary item widgets wrapper that filter by keyword

    Optional display SummaryItemWidget depend on summary is match by keyword or not

    Attributes:
        base_walker: Original SummaryListWalker
        keyword: Filter keyword
    """
    def __init__(self, base_walker, keyword):
        content = [m for m in base_walker if base_walker.displayer_context.displayer.match(keyword, m.message, m.get_title_as_plain_text())]
        super(FilterSummaryListWalker, self).__init__(
            content=content, base_walker=base_walker)
        self.keyword = keyword

    def recv(self, message):
        """ Action when received message from data store

        Will transform message into summary,
        and check message or summary is match by keyword or not,
        generate a SummaryItemWidget and display it if match
        """
        try:
            widget = self._create_widget(message)
            if self.displayer_context.displayer.match(self.keyword, message, widget.get_title_as_plain_text()):
                self.append(widget)
        except:
            self.controller.open_error()
        else:
            self.on_receive()

    def close(self):
        """ Unregister listener if quit search mode """
        self.displayer_context.store.unregister(self)

    def __delitem__(self, index):
        if isinstance(index, slice):
            for i in range(index.start, min(index.stop, len(self))):
                base_walker_index = self.base_walker.index(self[i])
                del self.base_walker[base_walker_index]
        else:
            base_walker_index = self.base_walker.index(self[index])
            del self.base_walker[base_walker_index]
        super(FilterSummaryListWalker, self).__delitem__(index)


class SummaryListWidget(BasicWidget):
    """ ListBox widget to contains the content of SummaryItemWidget

    Attributes:
        displayer_context: DisplayerContext
    """
    def __init__(self, displayer_context, **kwargs):
        super(SummaryListWidget, self).__init__(**kwargs)
        _verify_keys(displayer_context.actions)

        self.base_walker = SummaryListWalker(
            displayer_context=displayer_context,
            on_receive=self._on_receive, **kwargs)
        self.current_walker = self.base_walker

        self.search_widget = SearchWidget(self._filter, self._clear_search)
        self.help_widget = HelpWidget(
            HelpContent(
                [HelpCategory("Basic", self.context.config.keys),
                 HelpCategory("Advanced", _ADVANCED_KEYS),
                 make_category_with_actions("Custom", displayer_context.actions)]),
            **kwargs
        )

        self.display(urwid.ListBox(self.base_walker))

    def _filter(self, keyword):
        if keyword:
            new_walker = FilterSummaryListWalker(self.base_walker, keyword)
        else:
            new_walker = self.base_walker
        if new_walker is not self.current_walker:
            self._update_content(new_walker)
        self.controller._focus_body()

    def _update_content(self, walker):
        if self.current_walker is not self.base_walker:
            self.current_walker.close()

        self.current_walker = walker
        self.display(urwid.ListBox(walker))
        self._update_info()

    def _open_search(self):
        self.search_widget.clear()
        self.controller.open_edit(self.search_widget)

    def _clear_search(self):
        self._filter(None)
        self.controller.close_edit()

    def _update_info(self):
        if len(self.current_walker):
            curr_index = self._w.focus_position + 1
            total_index = len(self.current_walker)
            self.controller._update_info("[{0}/{1}]".format(
                curr_index, total_index))
        else:
            self.controller._update_info("[0/0]")

    def _on_receive(self):
        self._update_info()
        if self.context.config.auto_scroll:
            curr_index = self._w.focus_position + 1
            total_index = len(self.current_walker)
            if curr_index == total_index - 1:
                self._w.set_focus(curr_index)

    def keypress(self, size, key):
        if key == "/":
            self._open_search()
            return None
        if key == "q" and isinstance(self.current_walker, FilterSummaryListWalker):
            self._clear_search()
            return None
        if key == "q":
            self.controller.back()
            return None
        if key == "g":
            self._w.set_focus(0)
            self._update_info()
            return super(SummaryListWidget, self).keypress(size, key)
        if key == "G":
            self._w.set_focus(len(self.current_walker) - 1)
            self._update_info()
            return super(SummaryListWidget, self).keypress(size, key)
        if key == "x":
            del self.current_walker[self._w.focus_position]
            self._update_info()
            return super(SummaryListWidget, self).keypress(size, key)
        if key == "X":
            del self.current_walker[:]
            self._update_info()
            return super(SummaryListWidget, self).keypress(size, key)
        if key == "?":
            self.controller.open_view(self.help_widget)
            return None

        keypress_result = super(SummaryListWidget, self).keypress(size, key)  # pragma: no cover
        self._update_info()
        return keypress_result
