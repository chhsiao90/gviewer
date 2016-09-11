import unittest
import mock
from collections import OrderedDict

from ..util import render_to_text
from gviewer.view.helper import HelpWidget, HelpCategory, HelpContent, TitleWidget, MappingWidget


class TestHelpWidget(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.context = mock.Mock()
        self.widget = HelpWidget(
            HelpContent([
                HelpCategory("category1", OrderedDict([("a", "aaa"), ("b", "bbb")])),
                HelpCategory("category2", OrderedDict([("c", "ccc"), ("d", "ddd")]))]),
            controller=self.controller, context=self.context,)

    def test_render(self):
        self.assertEqual(
            render_to_text(self.widget, (20, 10)),
            [u"category1           ",
             u"                    ",
             u"     a   aaa        ",
             u"     b   bbb        ",
             u"                    ",
             u"category2           ",
             u"                    ",
             u"     c   ccc        ",
             u"     d   ddd        ",
             u"                    "])

    def test_quit(self):
        self.widget.keypress((0, ), "q")
        self.controller.back.assert_called_with()


class TestHelpCategory(unittest.TestCase):
    def test_max_key_length(self):
        category = HelpCategory(
            "category", dict(a="bbb", kkkkk="ddd"))
        self.assertEqual(category.max_key_length(), 5)


class TestTitleWidget(unittest.TestCase):
    def test_render(self):
        self.assertEqual(render_to_text(
            TitleWidget("title"), (5, )),
            [u"title"])


class TestMappingWidget(unittest.TestCase):
    def test_render(self):
        widget = MappingWidget("key", "value", 4)
        self.assertEqual(
            render_to_text(widget, (14, )),
            [u"     key value"])
