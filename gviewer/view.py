import urwid

from basic import BasicWidget, SearchWidget


class ViewWidget(BasicWidget):
    def __init__(self, message, index, parent):
        super(ViewWidget, self).__init__(parent)
        self.index = index
        self.message = message

        self.search_widget = SearchWidget(self.search, self.clear_search)

        _, view = parent.views[index]
        self.content_widget = self._make_widget(view)
        self.body = urwid.Pile([self.content_widget])

        header = Tabs(parent.view_names, self.index) if len(parent.view_names) else None

        widget = urwid.Frame(self.body, header=header)
        widget.set_focus("body")
        self.display(widget)

    def _make_widget(self, view):
        groups = view(self.message)
        return ListWidget(groups)

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

    def open_search(self):
        self.search_widget.clear()
        self.content_widget.clear_prev_search()
        if len(self.body.contents) == 1:
            self.body.contents.append((
                self.search_widget,
                self.body.options(height_type="pack"))
            )
        self.body.set_focus(self.search_widget)

    def close_search(self):
        if len(self.body.contents) == 2:
            del self.body.contents[1]

    def search(self, keyword):
        self.content_widget.search_next(keyword)
        self.close_search()

    def clear_search(self):
        self.search_widget.clear()
        self.close_search()

    def keypress(self, size, key):
        if self.body.get_focus() is self.search_widget:
            if key == "esc":
                self.close_search()
                return None
            else:
                return self.default_keypress(size, key)
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
            self.open_search()
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

        return super(ViewWidget, self).keypress(size, key)


class ItemWidget(BasicWidget):
    def __init__(self, item):
        widget = item.to_widget()
        super(ItemWidget, self).__init__(widget=widget)

    def search_next(self, keyword):
        try:
            return self._w.search_next(keyword)
        except AttributeError:
            pass

    def search_prev(self, keyword):
        try:
            return self._w.search_prev(keyword)
        except AttributeError:
            pass

    def clear_search(self):
        if self._w.clear_search:
            self._w.clear_search()


class ListWidget(urwid.WidgetWrap):
    def __init__(self, groups):
        widget = urwid.ListBox(self._make_walker(groups))
        super(ListWidget, self).__init__(widget)
        self._w.set_focus(0)
        self.prev_match = 0

    def _make_walker(self, groups):
        widgets = []
        for group in groups:
            widgets += group.to_widgets()
            widgets.append(EmptyLine())

        if not widgets:
            widgets.append(EmptyLine())

        walker = urwid.SimpleFocusListWalker(widgets)
        return walker

    def search_next(self, keyword):
        curr_index = self._w.get_focus()[1]
        if self.prev_match != curr_index:
            self.clear_prev_search()

        match_index = len(self._w.body) - 1
        for index in range(curr_index, len(self._w.body)):
            try:
                if self._w.body[index].search_next(keyword):
                    match_index = index
                    break
            except AttributeError:
                pass

        self.prev_match = match_index
        self._w.set_focus(match_index)

    def search_prev(self, keyword):
        curr_index = self._w.get_focus()[1]
        if self.prev_match != curr_index:
            self.clear_prev_search()

        match_index = 0
        for index in reversed(range(0, curr_index + 1)):
            try:
                if self._w.body[index].search_prev(keyword):
                    match_index = index
                    break
            except AttributeError:
                pass

        self.prev_match = match_index
        self._w.set_focus(match_index)

    def clear_prev_search(self):
        try:
            self._w.body[self.prev_match].clear_search()
        except AttributeError:
            pass


class TitleWidget(BasicWidget):
    def __init__(self, content):
        widget = urwid.Text(content)
        widget = urwid.AttrMap(widget, "view-title")
        super(TitleWidget, self).__init__(widget=widget)


class EmptyLine(urwid.Text):
    def __init__(self):
        super(EmptyLine, self).__init__("")


class Tabs(BasicWidget):
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
