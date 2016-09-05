import urwid
import sys

from ..basic_widget import BasicWidget, SearchableText
from ..action import Actions


def try_decode(text):
    if isinstance(text, str):
        return text.decode("utf8")
    if not isinstance(text, unicode):
        raise ValueError("not legal str: {0}".format(text))
    return text


class Base(object):  # pragma: no cover
    """Abstract class for view displayer eleemnt"""
    def to_widget(self, parent, context, message):
        raise NotImplementedError

    def text(self):
        return ""


class Text(Base):
    """One line detail content

    Attributes:
        content: str or unicode
    """
    def __init__(self, content):
        self.content = content

    def to_widget(self, parent, context, message):
        return SearchableText(self.content, attr_map="view-item")

    def text(self):
        return try_decode(self.content)


class Line(Text):
    """Lagacy interface

    Deprecated, for lagacy interface compatibility, would removed in the future
    Attributes:
        groups: iterable of Group
    """
    pass


class Prop(Base):
    """ Key-value property

    Attributes:
        key: str or unicode represent property key
        value: str or unicode represent property value
    """
    def __init__(self, key, value):
        self.kv = (key, value)
        self.max_key_length = 0

    def to_widget(self, parent, context, message):
        if self.max_key_length:
            format_str = "{0:" + str(self.max_key_length + 1) + "}: "
            return urwid.Text(
                [("view-item key", format_str.format(self.kv[0])),
                 ("view-item value", self.kv[1])])
        return urwid.Text(
            [("view-item key", self.kv[0] + ": "),
             ("view-item value", self.kv[1])])

    def text(self):
        if self.max_key_length:
            format_str = "{0:" + str(self.max_key_length + 1) + "}: {1}"
            text = format_str.format(self.kv[0], self.kv[1])
        else:
            text = "{0}: {1}".format(self.kv[0], self.kv[1])
        return try_decode(text)


class Group(object):
    """Group of view items

    Attributes:
        title: the group title
        items: iterable of Prop or Line
    """
    def __init__(self, title, items, show_title=True):
        self.title = title
        self.items = items
        self.show_title = show_title

    def to_widgets(self, parent, context, message):
        widgets = []
        if self.show_title:
            widgets.append(TitleWidget(self.title))
        widgets += [e.to_widget(parent, context, message) for e in self.items]
        return widgets

    def text(self):
        text = u"\n".join([e.text() for e in self.items])
        if self.show_title:
            text = try_decode(self.title) + u"\n" + text
        return text


class PropsGroup(Group):
    """Group of Prop

    Attributes:
        title: str or unicode
        items: iterable of Prop
    """
    def __init__(self, title, items, *args, **kwargs):
        max_key_length = max(map(lambda p: len(p.kv[0]), items))
        for p in items:
            p.max_key_length = max_key_length
        super(PropsGroup, self).__init__(title, items, *args, **kwargs)


class View(Base):
    """View Element

    Attributes:
        groups: iterable of Group
        actions: dict defined {key: callback}
    """
    def __init__(self, groups, actions=None):
        self.groups = groups
        self.actions = actions or Actions()

    def to_widget(self, parent, context, message):
        widgets = []
        for group in self.groups:
            widgets += group.to_widgets(parent, context, message)
            widgets.append(EmptyLine())

        if not widgets:
            widgets.append(EmptyLine())

        return ContentWidget(widgets, parent, context, message, self.actions)

    def text(self):
        return u"\n".join([g.text() + u"\n" for g in self.groups])


class Groups(View):
    """Lagacy interface

    Deprecated, for lagacy interface compatibility, would removed in the future
    Attributes:
        groups: iterable of Group
    """
    pass


class TitleWidget(BasicWidget):
    """Widget for title"""
    def __init__(self, content):
        widget = urwid.Text(content)
        super(TitleWidget, self).__init__(
            widget=widget,
            attr_map="view-title")


class ContentWidget(BasicWidget):
    """Widget for view items"""
    def __init__(self, widgets, parent, context, message, actions=None):
        walker = urwid.SimpleFocusListWalker(widgets)
        widget = urwid.ListBox(walker)
        super(ContentWidget, self).__init__(
            parent=parent,
            context=context,
            widget=widget)

        self.prev_match = 0

        self.message = message
        self.actions = actions or Actions()

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
            except AttributeError:  # pragma: no cover
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
            except AttributeError:  # pragma: no cover
                pass

        self.prev_match = match_index
        self._w.set_focus(match_index)

    def clear_prev_search(self):
        try:
            self._w.body[self.prev_match].clear()
        except AttributeError:  # pragma: no cover
            pass

    def keypress(self, size, key):
        if key in self.actions:
            try:
                self.actions[key].__call__(self.parent, self.message)
            except:  # pragma: no cover
                self.parent.open_error(sys.exc_info())
            return None
        return super(ContentWidget, self).keypress(size, key)


class EmptyLine(urwid.Text):
    def __init__(self):
        super(EmptyLine, self).__init__("")
