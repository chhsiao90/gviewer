import unittest
import urwid

try:
    import unittest.mock as mock
except:
    import mock

from gviewer.tests.util import render_to_content, render_widgets_to_content
from gviewer.basic import SearchableText
from gviewer.view.element import (
    Text, Prop, Group, PropsGroup, View,
    TitleWidget, ContentWidget, EmptyLine)
from gviewer.view.element import try_decode


class TextTest(unittest.TestCase):
    def test_to_widget(self):
        widget = Text("content").to_widget(None, None, None)
        self.assertTrue(isinstance(widget, SearchableText))
        self.assertEqual(
            widget.plain_text,
            u"content")

    def test_to_text(self):
        self.assertEqual(
            Text(b"content").text(), u"content")
        self.assertEqual(
            Text(u"content").text(), u"content")


class PropTest(unittest.TestCase):
    def test_to_widget(self):
        widget = Prop("key", "value").to_widget(None, None, None)
        text, attr = widget.get_text()
        self.assertEqual(
            text,
            "key: value"
        )
        self.assertEqual(
            attr,
            [("view-item key", 5),
             ("view-item value", 5)]
        )

    def test_to_widget_with_padding(self):
        prop = Prop("key", "value")
        prop.max_key_length = 5
        self.assertEqual(
            prop.to_widget(None, None, None).get_text()[0],
            "key   : value"
        )

    def test_to_text(self):
        self.assertEqual(
            Prop("key", "value").text(),
            u"key: value")

    def test_to_text_with_padding(self):
        prop = Prop("key", "value")
        prop.max_key_length = 5
        self.assertEqual(
            prop.text(),
            u"key   : value")


class GroupTest(unittest.TestCase):
    def test_to_widget_with_title(self):
        widgets = Group(
            "title",
            items=[
                Text("first line"),
                Text("second line")]
        ).to_widgets(None, None, None)

        self.assertEqual(len(widgets), 3)
        self.assertTrue(isinstance(widgets[0], TitleWidget))
        self.assertTrue(isinstance(widgets[1], SearchableText))
        self.assertTrue(isinstance(widgets[2], SearchableText))

    def test_to_widget_without_title(self):
        widgets = Group(
            "title",
            items=[
                Text("first line"),
                Text("second line")],
            show_title=False).to_widgets(None, None, None)

        self.assertEqual(len(widgets), 2)
        self.assertTrue(isinstance(widgets[0], SearchableText))
        self.assertTrue(isinstance(widgets[1], SearchableText))

    def test_to_text(self):
        self.assertEqual(
            Group("title", items=[Text("first line"), Text("second line")],
                  show_title=True).text(),
            u"title\nfirst line\nsecond line")

        self.assertEqual(
            Group("title", items=[Text("first line"), Text("second line")],
                  show_title=False).text(),
            u"first line\nsecond line")


class PropsGroupTest(unittest.TestCase):
    def test_calc_key_length(self):
        props_group = PropsGroup(
            "title",
            items=[
                Prop("key", "value"),
                Prop("longkey", "value"),
                Prop("k", "value")]
        )
        self.assertEqual(props_group.items[0].max_key_length, 7)
        self.assertEqual(props_group.items[1].max_key_length, 7)
        self.assertEqual(props_group.items[2].max_key_length, 7)


class ViewTest(unittest.TestCase):
    def test_to_widget(self):
        view = View([
            Group("group1", [Text("content1")]),
            Group("group2", [Text("content2")])]
        )
        widget = view.to_widget(None, None, None)
        self.assertTrue(isinstance(widget, ContentWidget))

        contents = widget._w.body
        self.assertEqual(len(contents), 6)
        self.assertIsInstance(contents[0], TitleWidget)
        self.assertIsInstance(contents[1], SearchableText)
        self.assertIsInstance(contents[2], EmptyLine)
        self.assertIsInstance(contents[3], TitleWidget)
        self.assertIsInstance(contents[4], SearchableText)
        self.assertIsInstance(contents[5], EmptyLine)

    def test_empty_widget(self):
        view = View([])
        contents = view.to_widget(None, None, None)._w.body
        self.assertEqual(len(contents), 1)
        self.assertIsInstance(contents[0], EmptyLine)

    def test_actions(self):
        action = mock.Mock()
        parent = mock.Mock()
        context = mock.Mock()
        context.config.keys = dict()

        view = View([
            Group("group1", [Text("content1")]),
            Group("group2", [Text("content2")])],
            actions=dict(a=action)
        )
        widget = view.to_widget(parent, context, "message")
        widget.keypress((0, 0), "a")
        action.assert_called_with(parent, "message")

        self.assertEqual(
            widget.keypress((0, 0), "b"),
            "b")

    def test_to_text(self):
        view = View([
            Group("group1", [Text("content1")]),
            Group("group2", [Text("content2")])]
        )
        self.assertEqual(
            view.text(),
            u"group1\ncontent1\n\ngroup2\ncontent2\n")


class TitleWidgetTest(unittest.TestCase):
    def test_render(self):
        widget = TitleWidget("content")
        contents = [c for c in widget.render((7,)).content()]
        self.assertEqual(len(contents), 1)
        self.assertEqual(len(contents[0]), 1)
        self.assertEqual(contents[0][0], ("view-title", None, "content"))


class ContentWidgetTest(unittest.TestCase):
    def test_search(self):
        widget = ContentWidget([
            SearchableText("this is aaa bbb"),
            SearchableText("this is ccc ddd"),
            SearchableText("this is eee aaa")
        ], None, None, None)

        no_match = render_widgets_to_content([
            urwid.Text("this is aaa bbb"),
            urwid.Text("this is ccc ddd"),
            urwid.Text("this is eee aaa")],
            (15, 3)
        )
        first_match = render_widgets_to_content([
            urwid.Text(["this is ", ("match", "aaa"), " bbb"]),
            urwid.Text("this is ccc ddd"),
            urwid.Text("this is eee aaa")],
            (15, 3)
        )
        second_match = render_widgets_to_content([
            urwid.Text("this is aaa bbb"),
            urwid.Text("this is ccc ddd"),
            urwid.Text(["this is eee ", ("match", "aaa")])],
            (15, 3)
        )

        self.assertEqual(
            render_to_content(widget, (15, 3)),
            no_match
        )

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            first_match
        )

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            second_match
        )

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            no_match
        )

        widget.search_prev("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            second_match
        )

        widget.search_prev("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            first_match
        )

        widget.search_prev("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            no_match
        )

    def test_search_next_before_move(self):
        widget = ContentWidget([
            SearchableText("this is aaa bbb"),
            SearchableText("this is ccc ddd"),
            SearchableText("this is eee aaa")
        ], None, None, None)

        no_match = render_widgets_to_content([
            urwid.Text("this is aaa bbb"),
            urwid.Text("this is ccc ddd"),
            urwid.Text("this is eee aaa")],
            (15, 3)
        )
        first_match = render_widgets_to_content([
            urwid.Text(["this is ", ("match", "aaa"), " bbb"]),
            urwid.Text("this is ccc ddd"),
            urwid.Text("this is eee aaa")],
            (15, 3)
        )
        second_match = render_widgets_to_content([
            urwid.Text("this is aaa bbb"),
            urwid.Text("this is ccc ddd"),
            urwid.Text(["this is eee ", ("match", "aaa")])],
            (15, 3)
        )

        self.assertEqual(
            render_to_content(widget, (15, 3)),
            no_match
        )

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            first_match
        )

        widget._w.focus_position = 2

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            second_match
        )

    def test_search_prev_before_move(self):
        widget = ContentWidget([
            SearchableText("this is aaa bbb"),
            SearchableText("this is ccc ddd"),
            SearchableText("this is eee aaa")
        ], None, None, None)

        no_match = render_widgets_to_content([
            urwid.Text("this is aaa bbb"),
            urwid.Text("this is ccc ddd"),
            urwid.Text("this is eee aaa")],
            (15, 3)
        )
        first_match = render_widgets_to_content([
            urwid.Text(["this is ", ("match", "aaa"), " bbb"]),
            urwid.Text("this is ccc ddd"),
            urwid.Text("this is eee aaa")],
            (15, 3)
        )
        second_match = render_widgets_to_content([
            urwid.Text("this is aaa bbb"),
            urwid.Text("this is ccc ddd"),
            urwid.Text(["this is eee ", ("match", "aaa")])],
            (15, 3)
        )

        self.assertEqual(
            render_to_content(widget, (15, 3)),
            no_match
        )

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            first_match
        )

        widget._w.focus_position = 2

        widget.search_prev("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            second_match
        )


class ElementTest(unittest.TestCase):
    def test_try_decode_failed(self):
        with self.assertRaises(ValueError):
            try_decode(dict())

    def test_try_decode_bytes_to_utf8(self):
        self.assertEqual(try_decode(b"aaa"), u"aaa")
