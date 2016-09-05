import unittest

try:
    import unittest.mock as mock
except:
    import mock

from ..util import render_to_text
from gviewer.view.helper import HelpWidget, HelpCategory, HelpContent, TitleWidget, MappingWidget


class HelpWidgetTest(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.context = mock.Mock()
        self.widget = HelpWidget(
            HelpContent([
                HelpCategory("category1", dict(a="aaa", b="bbb")),
                HelpCategory("category2", dict(c="ccc", d="ddd"))]),
            controller=self.controller, context=self.context,)

    def test_render(self):
        self.assertEqual(
            render_to_text(self.widget, (20, 10)),
            ["category1           ",
             "                    ",
             "     a   aaa        ",
             "     b   bbb        ",
             "                    ",
             "category2           ",
             "                    ",
             "     c   ccc        ",
             "     d   ddd        ",
             "                    "])

    def test_quit(self):
        self.widget.keypress((0, ), "q")
        self.controller.back.assert_called_with()


class HelpCategoryTest(unittest.TestCase):
    def test_max_key_length(self):
        category = HelpCategory(
            "category", dict(a="bbb", kkkkk="ddd"))
        self.assertEqual(category.max_key_length(), 5)


class TitleWidgetTest(unittest.TestCase):
    def test_render(self):
        self.assertEqual(render_to_text(
            TitleWidget("title"), (5, )),
            ["title"])


class MappingWidgetTest(unittest.TestCase):
    def test_render(self):
        widget = MappingWidget("key", "value", 4)
        self.assertEqual(
            render_to_text(widget, (14, )),
            ["     key value"])
