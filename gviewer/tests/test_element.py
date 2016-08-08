import unittest
import urwid

from gviewer.basic import SearchableText
from gviewer.element import Line, Prop, Group, PropsGroup, Groups
from gviewer.element import TitleWidget, ListWidget, EmptyLine


class LineTest(unittest.TestCase):
    def test_to_widget(self):
        widget = Line("content").to_widget()
        self.assertTrue(isinstance(widget, SearchableText))
        self.assertEqual(
            widget.plain_text,
            u"content")


class PropTest(unittest.TestCase):
    def test_to_widget(self):
        widget = Prop("key", "value").to_widget()
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
            prop.to_widget().get_text()[0],
            "key   : value"
        )


class GroupTest(unittest.TestCase):
    def test_to_widget_with_title(self):
        widgets = Group(
            "title",
            items=[
                Line("first line"),
                Line("second line")]
        ).to_widgets()

        self.assertEqual(len(widgets), 3)
        self.assertTrue(isinstance(widgets[0], TitleWidget))
        self.assertTrue(isinstance(widgets[1], SearchableText))
        self.assertTrue(isinstance(widgets[2], SearchableText))

    def test_to_widget_without_title(self):
        widgets = Group(
            "title",
            items=[
                Line("first line"),
                Line("second line")],
            show_title=False).to_widgets()

        self.assertEqual(len(widgets), 2)
        self.assertTrue(isinstance(widgets[0], SearchableText))
        self.assertTrue(isinstance(widgets[1], SearchableText))


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


class GroupsTest(unittest.TestCase):
    def test_to_widget(self):
        groups = Groups([
            Group("group1", [Line("content1")]),
            Group("group2", [Line("content2")])]
        )
        widget = groups.to_widget()
        self.assertTrue(isinstance(widget, ListWidget))

        contents = widget._w.body
        self.assertEqual(len(contents), 6)
        self.assertTrue(isinstance(contents[0], TitleWidget))
        self.assertTrue(isinstance(contents[1], SearchableText))
        self.assertTrue(isinstance(contents[2], EmptyLine))
        self.assertTrue(isinstance(contents[3], TitleWidget))
        self.assertTrue(isinstance(contents[4], SearchableText))
        self.assertTrue(isinstance(contents[5], EmptyLine))


class TitleWidgetTest(unittest.TestCase):
    def test_render(self):
        widget = TitleWidget("content")
        contents = [c for c in widget.render((7,)).content()]
        self.assertEqual(len(contents), 1)
        self.assertEqual(len(contents[0]), 1)
        self.assertEqual(contents[0][0], ("view-title", None, "content"))


class ListWidgetTest(unittest.TestCase):
    def test_search(self):
        widget = ListWidget([
            SearchableText("this is aaa bbb"),
            SearchableText("this is ccc ddd"),
            SearchableText("this is eee aaa")
        ])

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

    def test_search_before_move(self):
        widget = ListWidget([
            SearchableText("this is aaa bbb"),
            SearchableText("this is ccc ddd"),
            SearchableText("this is eee aaa")
        ])

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

        widget._w.set_focus(1)

        widget.search_next("aaa")
        self.assertEqual(
            render_to_content(widget, (15, 3)),
            second_match
        )


def render_to_content(widget, size):
    return [line for line in widget.render(size).content()]


def render_widgets_to_content(widgets, size):
    widget = urwid.ListBox(urwid.SimpleFocusListWalker(widgets))
    return render_to_content(widget, size)


if __name__ == "__main__":
    unittest.main()
