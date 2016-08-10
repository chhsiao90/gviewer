import urwid


def render_to_content(widget, size):
    return [line for line in widget.render(size).content()]


def render_widgets_to_content(widgets, size):
    widget = urwid.ListBox(urwid.SimpleFocusListWalker(widgets))
    return render_to_content(widget, size)
