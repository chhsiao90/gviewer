import unittest
from pygments.styles import get_all_styles
from pygments.styles import get_style_by_name

from gviewer.styles.util import (
    _PygmentsStyle, palette_from_pygments)


class TestPygmentsStyle(unittest.TestCase):
    def test_default(self):
        style = _PygmentsStyle("name")
        self.assertEqual(
            style.palette(),
            ("name", "default", "default"))

    def test_text_color_16(self):
        style = _PygmentsStyle("name")
        style.update("#f00")
        self.assertEqual(
            style.palette(),
            ("name", "light red", "default", None, "#f00", "default"))

    def test_text_color_256(self):
        style = _PygmentsStyle("name")
        style.update("#ff0000")
        self.assertEqual(
            style.palette(),
            ("name", "light red", "default", None, "#f00", "default"))

    def test_bold(self):
        style = _PygmentsStyle("name")
        style.update("bold")
        self.assertEqual(
            style.palette(),
            ("name", "bold,default", "default"))

    def test_text_bf_color_16(self):
        style = _PygmentsStyle("name")
        style.update("bg:#f00")
        style.update("#00f")
        self.assertEqual(
            style.palette(),
            ("name", "light blue", "light red", None, "#00f", "#f00"))

    def test_text_bg_color_256(self):
        style = _PygmentsStyle("name")
        style.update("bg:#ff0000")
        style.update("#00ff00")
        self.assertEqual(
            style.palette(),
            ("name", "light green", "light red", None, "#0f0", "#f00"))

    def test_text_bg_color_transparent(self):
        style = _PygmentsStyle("name")
        style.update("bg:")
        self.assertEqual(
            style.palette(),
            ("name", "default", "default"))


class TestStylesUtil(unittest.TestCase):
    def test_palette_from_pygments(self):
        for style_name in get_all_styles():
            palette = palette_from_pygments(get_style_by_name(style_name).styles)
            self.assertIsNotNone(palette)
            self.assertIsInstance(palette, list)
            self.assertTrue(len(palette))
