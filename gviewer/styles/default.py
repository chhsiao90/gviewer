from .util import palette_from_pygments

try:
    from pygments.styles import get_style_by_name
except:  # pragma: no cover
    pygments_style = []
else:
    pygments_style = palette_from_pygments(get_style_by_name("default"))

palette = [
    ("header", "white,bold", "dark green"),
    ("footer helper", "white,bold", "dark blue"),
    ("footer info", "white", "black"),
    ("summary", "white", "black"),
    ("summary focus", "black", "light gray"),
    ("view-item", "white", "black"),
    ("view-item key", "light cyan", "black"),
    ("view-item value", "white", "black"),
    ("view-title", "yellow,bold", "black"),
    ("tabs", "white,bold", "black"),
    ("tabs focus", "white,bold", "dark blue"),
    ("match", "black", "light gray"),
    ("help title", "white,bold", "black"),
    ("help key", "light cyan", "black"),
    ("help value", "white", "black")
] + pygments_style
