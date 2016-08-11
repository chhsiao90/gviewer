import urwid


def render_to_content(widget, size, focus=False):
    return [line for line in widget.render(size, focus).content()]


def render_widgets_to_content(widgets, size, focus=False):
    widget = urwid.ListBox(urwid.SimpleFocusListWalker(widgets))
    return render_to_content(widget, size, focus)
