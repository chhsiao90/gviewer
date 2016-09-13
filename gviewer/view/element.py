import urwid
from urwid.util import decompose_tagmarkup

from gviewer.action import Actions
from gviewer.basic_widget import BasicWidget, SearchableText
from gviewer.util import stringfy


class Base(object):  # pragma: no cover
    """Abstract class for view displayer eleemnt"""
    def widget(self, message, controller=None, context=None):
        raise NotImplementedError

    def __unicode__(self):
        raise NotImplementedError

    def __str__(self):
        return stringfy(self.__unicode__())

    def __bytes__(self):
        return self.__unicode__().encode("utf8")


class Text(Base):
    """One line detail content

    Attributes:
        content: str or unicode
    """
    def __init__(self, content):
        self.content = content

    def widget(self, message, controller=None, context=None):
        return SearchableText(self.content, attr_map="view-item")

    def __unicode__(self):
        if isinstance(self.content, bytes):
            return self.content.decode("utf8")
        elif isinstance(self.content, str):
            return self.content
        else:
            text, _ = decompose_tagmarkup(self.content)
            if isinstance(text, bytes):
                return text.decode("utf8")
            else:
                return text


class Prop(Base):
    """ Key-value property

    Attributes:
        key: str or unicode represent property key
        value: str or unicode represent property value
    """
    def __init__(self, key, value):
        self.kv = (key, value)
        self.max_key_length = 0

    def widget(self, message, controller=None, context=None):
        return SearchableText(
            [("view-item key", self.kv[0].ljust(self.max_key_length + 1) + ": "),
             ("view-item value", self.kv[1])])

    def __unicode__(self):
        return u"{0}: {1}".format(self.kv[0].ljust(self.max_key_length + 1), self.kv[1])


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

    def widgets(self, message, controller=None, context=None):
        widgets = []
        if self.show_title:
            widgets.append(TitleWidget(self.title))
        widgets += [e.widget(message, controller=controller, context=context) for e in self.items]
        return widgets

    def __unicode__(self):
        text = u"\n".join([str(e) for e in self.items])
        if self.show_title:
            text = self.title + u"\n" + text
        return text

    def __str__(self):
        return stringfy(self.__unicode__())

    def __bytes__(self):
        return self.__unicode__().encode("utf8")


class PropsGroup(Group):
    """Group of Prop

    Attributes:
        title: str or unicode
        items: iterable of Prop
    """
    def __init__(self, title, items, *args, **kwargs):
        if items:
            max_key_length = max(map(lambda p: len(p.kv[0]), items))
        else:
            max_key_length = 0
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

    def widget(self, message, controller=None, context=None):
        widgets = []
        for group in self.groups:
            widgets += group.widgets(message, controller=controller, context=context)
            widgets.append(EmptyLine())

        if not widgets:
            widgets.append(EmptyLine())

        return ContentWidget(
            widgets, message, self.actions, controller=controller,
            context=context)

    def __unicode__(self):
        return u"\n".join([str(g) + u"\n" for g in self.groups])


class TitleWidget(BasicWidget):
    """Widget for title"""
    def __init__(self, content):
        widget = urwid.Text(content)
        super(TitleWidget, self).__init__(
            widget=widget,
            attr_map="view-title")


class ContentWidget(BasicWidget):
    """Widget for view items"""
    def __init__(self, widgets, message, actions=None, controller=None, context=None):
        walker = urwid.SimpleFocusListWalker(widgets)
        widget = urwid.ListBox(walker)
        super(ContentWidget, self).__init__(
            controller=controller, context=context,
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
                self.actions[key].__call__(self.controller, self.message)
            except:  # pragma: no cover
                self.controller.open_error()
            return None
        return super(ContentWidget, self).keypress(size, key)


class EmptyLine(urwid.Text):
    def __init__(self):
        super(EmptyLine, self).__init__("")
