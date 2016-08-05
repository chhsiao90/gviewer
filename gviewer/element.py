import urwid
from basic import SearchableText
from view import TitleWidget, ItemWidget


class Base(object):
    def to_widget(self):
        raise NotImplementedError


class Line(Base):
    """
    One line detail content
    :param content: content
    :type content: str or unicode

    :param style: style name
    :type style: str
    """
    def __init__(self, content):
        self.content = content

    def to_widget(self):
        return SearchableWidget(self.content)


class SearchableWidget(urwid.WidgetWrap):
    def __init__(self, content):
        self.search_widget = SearchableText(content)
        widget = urwid.AttrMap(self.search_widget, "view-item")
        super(SearchableWidget, self).__init__(widget)

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


class Prop(object):
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
                [("view-item key", format_str.format(self.kv[0])),
                 ("view-item value", self.kv[1])])
        return urwid.Text(
            [("view-item key", self.kv[0] + ": "),
             ("view-item value", self.kv[1])])


class Group(object):
    """
    Group the detail content
    :param title: the group title
    :type title: str

    :param items: detail items
    :type items: iterable for Line or Prop
    """
    def __init__(self, title, items, show_title=True):
        self.title = title
        self.items = items
        self.show_title = show_title

    def to_widgets(self):
        widgets = []
        if self.show_title:
            widgets.append(TitleWidget(self.title))
        widgets += [ItemWidget(i) for i in self.items]
        return widgets


class PropsGroup(Group):
    def __init__(self, title, items, *args, **kwargs):
        max_key_length = max(map(lambda p: len(p.kv[0]), items))
        for p in items:
            p.max_key_length = max_key_length
        super(PropsGroup, self).__init__(title, items, *args, **kwargs)
