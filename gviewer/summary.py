import sys
import urwid

from basic import BasicWidget, FocusableText, SearchWidget


class SummaryItemWidget(BasicWidget):
    """ Summary item widget

    Summary item widget that display summary and defined action to open other view

    Attributes:
        parent: ParentFrame
        message: Original message genrate by BaseDataStore
        summary: Format message by displayer
    """
    def __init__(self, parent, message, summary):
        super(SummaryItemWidget, self).__init__(
            parent=parent,
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
        return key


class SummaryListWalker(urwid.SimpleFocusListWalker):
    """ Summary item widgets wrapper

    Contains the SummaryItemWidget,
    and used to receive message from data store

    Attributes:
        parent: ParentFrame
        content: Array of SummaryItemWidget
    """
    def __init__(self, parent, content=None):
        super(SummaryListWalker, self).__init__(content or [])
        self.parent = parent
        self.parent.msg_listener.register(self)

    def recv(self, message):
        """ Action when received message from data store

        Will transform message into summary,
        and generate a SummaryItemWidget into its content
        """
        try:
            summary = self.parent.displayer.summary(message)
            self.append(SummaryItemWidget(self.parent, message, summary))
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
        content = [m for m in origin_walker if parent.displayer.match(keyword, m.message, m.get_title())]
        super(FilterSummaryListWalker, self).__init__(parent, content=content)
        self.keyword = keyword

    def recv(self, message):
        """ Action when received message from data store

        Will transform message into summary,
        and check message or summary is match by keyword or not,
        generate a SummaryItemWidget and display it if matchj
        """
        try:
            summary = self.parent.displayer.summary(message)
            if self.parent.displayer.match(self.keyword, message, summary):
                self.append(SummaryItemWidget(self.parent, message, summary))
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
    """
    def __init__(self, walker, parent):
        super(SummaryListWidget, self).__init__(parent)
        self.base_walker = walker
        self.current_walker = walker
        self.list_box = urwid.ListBox(walker)
        self.search_widget = SearchWidget(self._filter, self._clear_search)

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

        return super(SummaryListWidget, self).keypress(size, key)
