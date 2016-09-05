import traceback
import urwid
import sys

from ..basic_widget import BasicWidget


class ErrorWidget(BasicWidget):
    """Widget for displaying exception info

    Attributes:
        exc_info: sys.exc_info()
    """
    def __init__(self, **kwargs):
        exc_info = sys.exc_info()
        contents = [
            urwid.Text(s.rstrip()) for s in traceback.format_exception(
                exc_info[0], exc_info[1], exc_info[2])]
        walker = urwid.SimpleFocusListWalker(contents)
        widget = urwid.ListBox(walker)
        super(ErrorWidget, self).__init__(
            widget=widget, attr_map="error", **kwargs)

    def keypress(self, size, key):
        if key == "q":
            self.controller.back()
            return None
        return super(ErrorWidget, self).keypress(size, key)  # pragma: no cover
