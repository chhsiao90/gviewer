import urwid


def render_to_content(widget, size, focus=False):
    return [line for line in widget.render(size, focus).content()]


def render_widgets_to_content(widgets, size, focus=False, inline=False):
    if inline:
        widget = urwid.Columns([("pack", w) for w in widgets])
    else:
        widget = urwid.Pile([("pack", w) for w in widgets])
    return render_to_content(widget, size, focus)


def render_to_text(widget, size, focus=False):
    return list(map(lambda t: t.decode("utf8"), widget.render(size, focus).text))
