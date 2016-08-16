import traceback
import urwid

from basic import BasicWidget


class ErrorWidget(BasicWidget):
    """Widget for displaying exception info

    Attributes:
        parent: ParentFrame instance
        exc_info: sys.exc_info()
    """
    def __init__(self, parent, exc_info):
        contents = [
            urwid.Text(s.rstrip()) for s in traceback.format_exception(
                exc_info[0], exc_info[1], exc_info[2])]
        walker = urwid.SimpleFocusListWalker(contents)
        widget = urwid.ListBox(walker)
        super(ErrorWidget, self).__init__(
            parent=parent,
            widget=widget,
            attr_map="error")

    def keypress(self, size, key):
        if key == "q":
            self.parent.open_summary()
            return None
        return super(ErrorWidget, self).keypress(size, key)
