import traceback
import urwid

from basic import BasicWidget


class ErrorWidget(BasicWidget):
    def __init__(self, parent, exc_info):
        contents = [
            urwid.Text(s.rstrip()) for s in traceback.format_exception(
                exc_info[0], exc_info[1], exc_info[2])]
        walker = urwid.SimpleFocusListWalker(contents)
        widget = urwid.ListBox(walker)
        widget = urwid.AttrMap(widget, "error")
        super(ErrorWidget, self).__init__(parent, widget)
