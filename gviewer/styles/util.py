COLOR256_TO_BASIC = dict([
    ((0, 0, 0), "black"),
    ((0, 0, 1), "dark blue"),
    ((0, 0, 2), "light blue"),
    ((0, 1, 0), "dark green"),
    ((0, 1, 1), "dark cyan"),
    ((0, 1, 2), "dark cyan"),
    ((0, 2, 0), "light green"),
    ((0, 2, 1), "dark cyan"),
    ((0, 2, 2), "light cyan"),
    ((1, 0, 0), "dark red"),
    ((1, 0, 1), "dark magenta"),
    ((1, 0, 2), "dark magenta"),
    ((1, 1, 0), "brown"),
    ((1, 1, 1), "dark gray"),
    ((1, 1, 2), "light blue"),
    ((1, 2, 0), "brown"),
    ((1, 2, 1), "light green"),
    ((1, 2, 2), "light cyan"),
    ((2, 0, 0), "light red"),
    ((2, 0, 1), "dark magenta"),
    ((2, 0, 2), "light magenta"),
    ((2, 1, 0), "brown"),
    ((2, 1, 1), "light red"),
    ((2, 1, 2), "light magenta"),
    ((2, 2, 0), "yellow"),
    ((2, 2, 1), "yellow"),
    ((2, 2, 2), "white")
])


def palette_from_pygments(style):
    original_palettes = dict()
    for k, v in style.styles.items():
        if v:
            original_palettes[k] = _parse_pygments_style(v)

    palettes = original_palettes.copy()
    for token, style in original_palettes.items():
        _enrich_pygments_style_subtypes(palettes, token, style)

    palettes_list = []
    for k, v in palettes.items():
        palette = [k]
        palette.extend(v)
        palettes_list.append(palette)
    return palettes_list


class _PygmentsStyle(object):
    def __init__(self):
        self.text_color = "default"
        self.bg_color = "default"
        self.styles = []
        self.high_text_color = None
        self.high_bg_color = "default"

    def update(self, value):
        if value == "bold":
            self.styles.append(value)
        elif value == "bg:":
            pass
        elif value.startswith("bg:"):
            low_color, high_color = _parse_pygments_color(value[3:])
            self.bg_color = low_color
            self.high_bg_color = high_color
        elif value.startswith("#"):
            low_color, high_color = _parse_pygments_color(value)
            self.text_color = low_color
            self.high_text_color = high_color

    def palette(self):
        if self.high_text_color:
            return (",".join(self.styles + [self.text_color]),
                    self.bg_color, None, self.high_text_color, self.high_bg_color)
        else:
            return (",".join(self.styles + [self.text_color]),
                    self.bg_color)


def _parse_pygments_color(value):
    if len(value) == 4:
        r = int(value[1], base=16)
        g = int(value[2], base=16)
        b = int(value[3], base=16)
        low_color = COLOR256_TO_BASIC.get((
            int(r * 3 / 16), int(g * 3 / 16), int(b * 3 / 16)))
        return low_color, value
    elif len(value) == 7:
        r = int(value[1:3], base=16)
        g = int(value[3:5], base=16)
        b = int(value[5:7], base=16)
        low_color = COLOR256_TO_BASIC.get((
            int(r * 3 / 256), int(g * 3 / 256), int(b * 3 / 256)))
        high_color = "#{0}{1}{2}".format(
            hex(int(r / 16))[2], hex(int(g / 16))[2], hex(int(b / 16))[2])
        return low_color, high_color
    else:  # pragma: no cover
        raise ValueError("not legal color code: {0}".format(value))


def _parse_pygments_style(style_value):
    style = _PygmentsStyle()
    for style_item in style_value.split(" "):
        style.update(style_item)
    return style.palette()


def _enrich_pygments_style_subtypes(palettes, token, style):
    if token not in palettes:
        palettes[token] = style
    for child_token in token.subtypes:
        _enrich_pygments_style_subtypes(palettes, child_token, style)
