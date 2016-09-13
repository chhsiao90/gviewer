from gviewer.styles.util import palette_from_pygments

try:
    from pygments.styles import get_style_by_name
except:  # pragma: no cover
    pygments_style = []
else:
    pygments_style = palette_from_pygments(get_style_by_name("default"))

palette = [
    ("normal", "white", "black"),
    ("em", "white,bold", "black"),
    ("header", "white,bold", "dark green"),
    ("footer helper", "white,bold", "dark blue"),
    ("footer info", "white", "black"),
    ("summary", "normal"),
    ("summary focus", "black", "light gray"),
    ("view-item", "normal"),
    ("view-item key", "light cyan", "black"),
    ("view-item value", "normal"),
    ("view-title", "yellow,bold", "black"),
    ("tabs", "em"),
    ("tabs focus", "white,bold", "dark blue"),
    ("match", "black", "light gray"),
    ("help title", "em"),
    ("help key", "light cyan", "black"),
    ("help value", "normal"),
    ("red", "light red", "black")
] + pygments_style
