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
    def __init__(self, message, index, parent):
        super(DetailWidget, self).__init__(parent)
        self.index = index
        self.message = message

        _, detail_displayer = parent.detail_displayers[index]

        body = self._make_body(detail_displayer)
        header = Tabs(parent.detail_names, self.index) \
            if len(parent.detail_names) > 1 \
            else None
        widget = urwid.Frame(body, header=header)
        self.display(widget)

    def _make_body(self, detail_displayer):
        detail_groups = detail_displayer \
            .to_detail_groups(self.message)
        widgets = []
        for group in detail_groups:
            widgets.append(DetailTitleWidget(group.title))
            widgets += [DetailItemWidget(i) for i in group.items]
            widgets.append(EmptyLine())

        walker = urwid.SimpleFocusListWalker(widgets)
        return urwid.ListBox(walker)

    def _next_view(self):
        if len(self.parent.detail_names) == 1:
            return

        if len(self.parent.detail_names) > self.index + 1:
            next_index = self.index + 1
        else:
            next_index = 0
        self.parent.open_detail(self.message, next_index)

    def keypress(self, size, key):
        if key == "tab":
            self._next_view()
            return None
        return super(DetailWidget, self).keypress(size, key)


class DetailLine(object):
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
        widget = urwid.Text(self.content)
        return urwid.AttrMap(widget, "detailitem")


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
            format_str = "{0:" + str(self.max_key_length) + "}: "
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
    def __init__(self, title, items):
        self.title = title
        self.items = items


class DetailItemWidget(BasicWidget):
    def __init__(self, item):
        widget = item.to_widget()
        super(DetailItemWidget, self).__init__(widget=widget)


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
