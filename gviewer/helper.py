import urwid

from basic import BasicWidget


class HelpWidget(BasicWidget):
    """Help widget that show help message

    Attributes:
        parent: ParentFrame
        widget: ListBox widget contains help messages
    """
    def __init__(self, parent, help_content):
        super(HelpWidget, self).__init__(
            parent=parent)
        widget = self._widget(help_content)
        self.display(widget)

    def _widget(self, help_content):
        widgets = []
        for category in help_content.categories:
            widgets.append(TitleWidget(category.name))
            widgets.append(urwid.Text(""))

            padding = category.max_key_length() + 3
            mapping_widgets = [MappingWidget(k, v, padding) for k, v in category.mappings.iteritems()]
            widgets = widgets + mapping_widgets

        walker = urwid.SimpleFocusListWalker(widgets)
        return urwid.ListBox(walker)

    def keypress(self, size, key):
        if key == "q":
            self.parent.open_summary()
            return None
        return super(HelpWidget, self).keypress(size, key)


class HelpContent(object):
    """Help content"""
    def __init__(self, categories):
        self.categories = categories


class HelpCategory(object):
    """Help category"""
    def __init__(self, name, mappings):
        self.name = name
        self.mappings = mappings

    def max_key_length(self):
        try:
            return max([len(k) for k in self.mappings.iterkeys()])
        except:
            return 0


class TitleWidget(BasicWidget):
    """Title for each category"""
    def __init__(self, title):
        super(TitleWidget, self).__init__(
            widget=urwid.Text(title),
            attr_map="help title"
        )


class MappingWidget(BasicWidget):
    """Widget list the functionality of each key"""
    def __init__(self, key, value, padding):
        key_with_padding = ("{0:" + str(padding) + "}").format(key)
        widget = urwid.Text(
            [("help key", key_with_padding),
             ("help value", value)]
        )
        widget = urwid.Padding(
            widget,
            width="pack",
            left=5)
        super(MappingWidget, self).__init__(
            widget=widget)
