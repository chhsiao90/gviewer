import urwid


""" Detail Widget Related Component

Contents:

* `Detail`: ListBox to display detail
* `Prop`: Each line of the detail
* `PropSeparator`: Seperator between properties group
* `EmptyLine`: Empty Line

"""


class Detail(urwid.WidgetWrap):
    def __init__(self, displayer, message):
        super(Detail, self).__init__(self._make_widget(displayer, message))

    def _make_widget(self, displayer, message):
        detail_groups = displayer.to_detail_groups(message)
        widgets = []
        for gk, gv in detail_groups:
            widgets.append(PropSeparator(gk))
            widgets += [Prop(t) for t in gv]
            widgets.append(EmptyLine())

        walker = urwid.SimpleFocusListWalker(widgets)
        return urwid.ListBox(walker)


class Prop(urwid.WidgetWrap):
    def __init__(self, content):
        if isinstance(content, tuple):
            key, value = content
            text = u"{0}: {1}".format(key, value)
        else:
            text = content
        w = urwid.AttrMap(
            urwid.Text(text), "prop", "prop focus")
        super(Prop, self).__init__(w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class PropSeparator(urwid.WidgetWrap):
    def __init__(self, content):
        super(PropSeparator, self).__init__(
            urwid.AttrMap(urwid.Text(content), "prop separator"))


class EmptyLine(urwid.Text):
    def __init__(self):
        super(EmptyLine, self).__init__("")
