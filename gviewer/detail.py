import urwid

from basic import BasicWidget
from search import SearchableText, SearchWidget

""" Detail Widget Related Component

Contents:

* `DetailWidget`: ListBox to display detail
* `DetailTitleWidget`: Title for detail group
* `DetailItemWidget`: Each line of the detail item
* `DetailGroup`: define detail group that contains title and content
* `PropsDetailGroup`: define detail group that contains title and key-value prop content
* `EmptyLine`: Empty Line
* `DetailLine`: detail line
* `DetailProp`: detail properties
* `Tabs`: tabs

"""


class DetailWidget(BasicWidget):
    def __init__(self, message, index, parent):
        super(DetailWidget, self).__init__(parent)
        self.index = index
        self.message = message

        self.search_widget = SearchWidget(self.search, self.clear_search)

        _, detail_displayer = parent.detail_displayers[index]
        self.detail_content = self._make_widget(detail_displayer)
        self.body = urwid.Pile([self.detail_content])

        header = Tabs(parent.detail_names, self.index) if len(parent.detail_names) else None

        widget = urwid.Frame(self.body, header=header)
        self.display(widget)

    def _make_widget(self, detail_displayer):
        detail_groups = detail_displayer(self.message)
        return DetailListWidget(detail_groups)

    def _next_view(self):
        if len(self.parent.detail_names) == 1:
            return

        if len(self.parent.detail_names) > self.index + 1:
            next_index = self.index + 1
        else:
            next_index = 0
        self.parent.open_detail(self.message, next_index)

    def _prev_view(self):
        if len(self.parent.detail_names) == 1:
            return

        next_index = len(self.parent.detail_names) - 1 if self.index == 0 else self.index - 1
        self.parent.open_detail(self.message, next_index)

    def open_search(self):
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
        self.detail_content.search_next(keyword)
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
            self.parent.to_summary()
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
                self.detail_content.search_next(
                    self.search_widget.get_keyword()
                )
            return None
        if key == "N":
            if self.search_widget.get_keyword():
                self.detail_content.search_prev(
                    self.search_widget.get_keyword()
                )
            return None

        return super(DetailWidget, self).keypress(size, key)


class DetailLine(urwid.WidgetWrap):
    """
    One line detail content
    :param content: content
    :type content: str or unicode

    :param style: style name
    :type style: str
    """
    def __init__(self, content):
        self.search_widget = SearchableText(content)
        widget = urwid.AttrMap(self.search_widget, "detailitem")
        super(DetailLine, self).__init__(widget)

    def search_next(self, keyword):
        if self.search_widget.search_next(keyword):
            return True
        return False

    def search_prev(self, keyword):
        if self.search_widget.search_prev(keyword):
            return True
        return False

    def clear_search(self):
        self.search_widget.clear()

    def to_widget(self):
        return self


class DetailProp(object):
    """
    One line detail content
    :param key: property key
    :type key: str or unicode

    :param value: property value
    :type value: str or unicode

    :param style: style name
    :type style: str
    """
    def __init__(self, key, value):
        self.kv = (key, value)
        self.max_key_length = 0

    def to_widget(self):
        if self.max_key_length:
            format_str = "{0:" + str(self.max_key_length + 1) + "}: "
            return urwid.Text(
                [("detailitem key", format_str.format(self.kv[0])),
                 ("detailitem value", self.kv[1])])
        return urwid.Text(
            [("detailitem key", self.kv[0] + ": "),
             ("detailitem value", self.kv[1])])


class DetailGroup(object):
    """
    Group the detail content
    :param title: the group title
    :type title: str

    :param items: detail items
    :type items: iterable for DetailLine or DetailProp
    """
    def __init__(self, title, items, show_title=True):
        self.title = title
        self.items = items
        self.show_title = show_title

    def to_widgets(self):
        widgets = []
        if self.show_title:
            widgets.append(DetailTitleWidget(self.title))
        widgets += [DetailItemWidget(i) for i in self.items]
        return widgets


class PropsDetailGroup(DetailGroup):
    def __init__(self, title, items, *args, **kwargs):
        max_key_length = max(map(lambda p: len(p.kv[0]), items))
        for p in items:
            p.max_key_length = max_key_length
        super(PropsDetailGroup, self).__init__(title, items, *args, **kwargs)


class DetailItemWidget(BasicWidget):
    def __init__(self, item):
        widget = item.to_widget()
        super(DetailItemWidget, self).__init__(widget=widget)

    def search_next(self, keyword):
        try:
            return self._w.search_next(keyword)
        except:
            pass

    def search_prev(self, keyword):
        try:
            return self._w.search_prev(keyword)
        except:
            pass

    def clear_search(self):
        if self._w.clear_search:
            self._w.clear_search()


class DetailListWidget(urwid.WidgetWrap):
    def __init__(self, detail_groups):
        widget = urwid.ListBox(self._make_walker(detail_groups))
        super(DetailListWidget, self).__init__(widget)
        self.curr_match = 0

    def _make_walker(self, detail_groups):
        widgets = []
        for group in detail_groups:
            widgets += group.to_widgets()
            widgets.append(EmptyLine())

        walker = urwid.SimpleFocusListWalker(widgets)
        return walker

    def search_next(self, keyword):
        for index in range(self.curr_match, len(self._w.body)):
            try:
                if self._w.body[index].search_next(keyword):
                    self.curr_match = index
                    break
            except:
                pass

    def search_prev(self, keyword):
        for index in reversed(range(0, self.curr_match + 1)):
            try:
                if self._w.body[index].search_prev(keyword):
                    self.curr_match = index
                    break
            except:
                pass


class DetailTitleWidget(BasicWidget):
    def __init__(self, content):
        widget = urwid.Text(content)
        widget = urwid.AttrMap(widget, "detailtitle")
        super(DetailTitleWidget, self).__init__(widget=widget)


class EmptyLine(urwid.Text):
    def __init__(self):
        super(EmptyLine, self).__init__("")


class Tabs(BasicWidget):
    def __init__(self, detail_names, index):
        widget = self._make_widget(detail_names, index)
        super(Tabs, self).__init__(widget=widget)

    def _make_widget(self, detail_names, index):
        def make_tab(curr_index):
            name = detail_names[curr_index]
            if curr_index == index:
                return urwid.AttrMap(urwid.Text(name), "tabs focus")
            return urwid.AttrMap(urwid.Text(name), "tabs")
        widgets = map(make_tab, range(0, len(detail_names)))
        return urwid.Columns(widgets)
