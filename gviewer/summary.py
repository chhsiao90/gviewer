import sys
import urwid
from collections import OrderedDict

from basic import BasicWidget, FocusableText, SearchWidget
from helper import (
    HelpWidget, HelpContent, HelpCategory,
    make_category_with_actions)


_ADVANCED_KEYS = OrderedDict([
    ("/", "search"),
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
        parent: ParentFrame
        context: Context
        message: Original message genrate by BaseDataStore
        summary: Format message by displayer
    """
    def __init__(self, parent, context, message, summary):
        super(SummaryItemWidget, self).__init__(
            parent=parent,
            context=context,
            widget=FocusableText(
                summary,
                attr_map="summary",
                focus_map="summary focus")
        )

        self.message = message

    def get_title(self):
        """ Get summary in plain text

        Returns:
            summary in plain text
        """
        return self._w.get_plain_text()

    def keypress(self, size, key):
        if key == "enter":
            self.parent.display_view(self.message, 0)
            return None
        if key in self.context.summary_actions:
            try:
                self.context.summary_actions[key].__call__(
                    self.parent, self.message)
            except:  # pragma: no cover
                self.parent.open_error(sys.exc_info())
            return None

        return super(SummaryItemWidget, self).keypress(size, key)  # pragma: no cover


class SummaryListWalker(urwid.SimpleFocusListWalker):
    """ Summary item widgets wrapper

    Contains the SummaryItemWidget,
    and used to receive message from data store

    Attributes:
        parent: ParentFrame
        context: Context
        context: Context
        content: list of SummaryItemWidget
    """
    def __init__(self, parent, context, content=None):
        super(SummaryListWalker, self).__init__(content or [])
        self.parent = parent
        self.context = context
        self.parent.msg_listener.register(self)

    def recv(self, message):
        """ Action when received message from data store

        Will transform message into summary,
        and generate a SummaryItemWidget into its content
        """
        try:
            summary = self.context.displayer.summary(message)
            self.append(SummaryItemWidget(self.parent, self.context, message, summary))
        except:
            self.parent.open_error(sys.exc_info())


class FilterSummaryListWalker(SummaryListWalker):
    """ Summary item widgets wrapper that filter by keyword

    Optional display SummaryItemWidget depend on summary is match by keyword or not

    Attributes:
        origin_walker: Original SummaryListWalker
        keyword: Filter keyword
    """
    def __init__(self, origin_walker, keyword):
        parent = origin_walker.parent
        context = origin_walker.context
        content = [m for m in origin_walker if context.displayer.match(keyword, m.message, m.get_title())]
        super(FilterSummaryListWalker, self).__init__(parent, context, content=content)
        self.keyword = keyword

    def recv(self, message):
        """ Action when received message from data store

        Will transform message into summary,
        and check message or summary is match by keyword or not,
        generate a SummaryItemWidget and display it if match
        """
        try:
            summary = self.context.displayer.summary(message)
            widget = SummaryItemWidget(self.parent, self.context, message, summary)
            if self.context.displayer.match(self.keyword, message, widget.get_title()):
                self.append(widget)
        except:
            self.parent.open_error(sys.exc_info())

    def close(self):
        """ Unregister listener if quit search mode """
        self.parent.msg_listener.unregister(self)


class SummaryListWidget(BasicWidget):
    """ ListBox widget to contains the content of SummaryItemWidget

    Attributes:
        walker: SummaryListWalker instance
        parent: ParentFrame instance
        context: Context
    """
    def __init__(self, walker, parent, context):
        super(SummaryListWidget, self).__init__(
            parent=parent, context=context)
        _verify_keys(self.context.summary_actions)

        self.base_walker = walker
        self.current_walker = walker
        self.list_box = urwid.ListBox(walker)

        self.search_widget = SearchWidget(self._filter, self._clear_search)
        self.help_widget = HelpWidget(
            parent, context,
            HelpContent(
                [HelpCategory("Basic", self.context.config.keys),
                 HelpCategory("Advanced", _ADVANCED_KEYS),
                 make_category_with_actions("Custom", self.context.summary_actions)])
        )

        widget_list = [self.list_box]
        widget = urwid.Pile(widget_list)
        self.display(widget)

    def _filter(self, keyword):
        if keyword:
            new_walker = FilterSummaryListWalker(self.base_walker, keyword)
        else:
            new_walker = self.base_walker

        if new_walker is not self.current_walker:
            self._update(new_walker)

        self._close_search()
        self._w.focus_position = 0

    def _update(self, walker):
        if self.current_walker is not self.base_walker:
            self.current_walker.close()

        self.current_walker = walker
        self._w.contents.pop(0)
        self._w.contents.insert(0, (urwid.ListBox(walker), self._w.options()))

    def _open_search(self):
        self.search_widget.clear()
        if len(self._w.contents) == 1:
            self._w.contents.append((
                self.search_widget,
                self._w.options(height_type="pack"))
            )
        self._w.focus_position = 1

    def _close_search(self):
        if len(self._w.contents) == 2:
            del self._w.contents[1]

    def _clear_search(self):
        self._filter(None)

    def is_editing(self):
        return self._w.focus is self.search_widget

    def keypress(self, size, key):
        if self.is_editing():
            return super(SummaryListWidget, self).keypress(size, key)
        if key == "/":
            self._open_search()
            return None
        if key == "q" and isinstance(self.current_walker, FilterSummaryListWalker):
            self._clear_search()
            return None
        if key == "?":
            self.parent.open(self.help_widget)
            return None

        return super(SummaryListWidget, self).keypress(size, key)  # pragma: no cover
