import urwid

from basic import BasicWidget

""" Detail Widget Related Component

Contents:

* `DetailWidget`: ListBox to display detail
* `DetailItemWidget`: Each line of the detail
* `DetailItemSeparator`: Seperator between properties group
* `EmptyLine`: Empty Line
* `DetailLine`: detail line
* `DetailProp`: detail properties
* `DetailGroup`: detail group

"""


class DetailWidget(BasicWidget):
    def __init__(self, message, **kwargs):
        displayer = kwargs["parent"].displayer
        super(DetailWidget, self).__init__(self._make_widget(displayer, message), **kwargs)

    def _make_widget(self, displayer, message):
        detail_groups = displayer.to_detail_groups(message)
        widgets = []
        for group in detail_groups:
            widgets.append(DetailItemSeparator(group.title))
            widgets += [DetailItemWidget(i) for i in group.items]
            widgets.append(EmptyLine())

        walker = urwid.SimpleFocusListWalker(widgets)
        return urwid.ListBox(walker)


class DetailLine(object):
    """
    One line detail content
    :param content: content
    :type content: str or unicode

    :param style: style name
    :type style: str
    """
    def __init__(self, content, style=None):
        self.content = content
        self.style = style


class DetailProp(DetailLine):
    """
    One line detail content
    :param key: property key
    :type key: str or unicode

    :param value: property value
    :type value: str or unicode

    :param style: style name
    :type style: str
    """
    def __init__(self, key, value, style=None):
        super(DetailProp, self).__init__(u"{0}: {1}".format(key, value), style)


class DetailGroup(object):
    """
    Group the detail content
    :param title: the group title
    :type title: str

    :param items: detail items
    :type items: iterable for DetailLine or DetailProp
    """
    def __init__(self, title, items):
        self.title = title
        self.items = items


class DetailItemWidget(BasicWidget):
    def __init__(self, item):
        w = urwid.AttrMap(
            urwid.Text(item.content), item.style or "detailitem")
        super(DetailItemWidget, self).__init__(w)

    def keypress(self, size, key):
        return key


class DetailItemSeparator(BasicWidget):
    def __init__(self, content):
        super(DetailItemSeparator, self).__init__(
            urwid.AttrMap(urwid.Text(content), "detailitem separator"))


class EmptyLine(urwid.Text):
    def __init__(self):
        super(EmptyLine, self).__init__("")
