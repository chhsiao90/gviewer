import unittest
import urwid

try:
    import unittest.mock as mock
except:
    import mock

from gviewer.tests.util import render_to_content, render_widgets_to_content
from gviewer.view.widget import ViewWidget, Tabs
from gviewer.view.element import Line, Group, Groups


class ViewWidgetTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()

        self.parent.views = [
            ("View 1", lambda m: self._display(m["view1"])),
            ("View 2", lambda m: self._display(m["view2"])),
            ("View 3", lambda m: self._display(m["view3"]))
        ]
        self.parent.view_names = [
            e[0] for e in self.parent.views
        ]
        self.parent.open_summary = mock.Mock()

        self.test_message = dict(view1="view1", view2="view2", view3="view3")

    def _view1(self, message):
        return self._display(message["view1"])

    def _view2(self, message):
        return self._display(message["view2"])

    def _display(self, message):
        return Groups([Group("Title", [Line(message)])])

    def test_render(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)

        self.assertEqual(
            render_to_content(widget._w.contents["body"][0], (7, 2)),
            render_widgets_to_content([
                urwid.AttrMap(urwid.Text("Title"), "view-title"),
                urwid.AttrMap(urwid.Text("view1"), "view-item")
            ], (7, 2))
        )

    def test_next_view(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)
        widget.keypress((0,), "tab")
        self.parent.display_view.assert_called_with(
            self.test_message, 1)

        widget = ViewWidget(
            self.test_message,
            1, self.parent)
        widget.keypress((0,), "tab")
        self.parent.display_view.assert_called_with(
            self.test_message, 2)

        widget = ViewWidget(
            self.test_message,
            2, self.parent)
        widget.keypress((0,), "tab")
        self.parent.display_view.assert_called_with(
            self.test_message, 0)

    def test_prev_view(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)
        widget.keypress((0,), "shift tab")
        self.parent.display_view.assert_called_with(
            self.test_message, 2)

        widget = ViewWidget(
            self.test_message,
            2, self.parent)
        widget.keypress((0,), "shift tab")
        self.parent.display_view.assert_called_with(
            self.test_message, 1)

        widget = ViewWidget(
            self.test_message,
            1, self.parent)
        widget.keypress((0,), "shift tab")
        self.parent.display_view.assert_called_with(
            self.test_message, 0)

    def test_no_tab(self):
        self.parent.view_names = [self.parent.view_names[0]]
        widget = ViewWidget(
            self.test_message,
            0, self.parent)

        with self.assertRaises(KeyError):
            widget._w.contents["header"]

    def test_open_search(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)

        widget.keypress((0,), "/")
        self.assertEqual(
            widget.body.contents[1][0],
            widget.search_widget)
        self.assertIs(widget.body.focus, widget.search_widget)

    def test_close_search(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)

        self.assertEqual(len(widget.body.contents), 1)
        widget._close_search()
        self.assertEqual(len(widget.body.contents), 1)
        widget._open_search()
        self.assertEqual(len(widget.body.contents), 2)
        widget._close_search()
        self.assertEqual(len(widget.body.contents), 1)

    def test_open_summary(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)

        widget.keypress((0,), "q")
        self.parent.open_summary.assert_called_with()

    def test_search(self):
        widget = ViewWidget(
            self.test_message,
            0, self.parent)

        widget.search_widget.keypress((4,), "v")
        widget.search_widget.keypress((4,), "i")
        widget.search_widget.keypress((4,), "e")
        widget.search_widget.keypress((4,), "w")
        widget.search_widget.keypress((4,), "enter")

        match = render_widgets_to_content(
            [urwid.Text(("view-title", "Title")),
             urwid.Text([("match", "view"), ("view-item", "1")])],
            (5, 3)
        )
        no_match = render_widgets_to_content(
            [urwid.Text(("view-title", "Title")),
             urwid.Text(("view-item", "view1"))],
            (5, 3)
        )

        self.assertEqual(
            render_to_content(widget.content_widget, (5, 3)),
            match)

        widget.keypress((0,), "n")
        self.assertEqual(
            render_to_content(widget.content_widget, (5, 3)),
            no_match)

        widget.keypress((0,), "N")
        self.assertEqual(
            render_to_content(widget.content_widget, (5, 3)),
            match)

        widget.keypress((0,), "N")
        self.assertEqual(
            render_to_content(widget.content_widget, (5, 3)),
            no_match)


class TabsTest(unittest.TestCase):
    def test_render(self):
        widget = Tabs(
            ["view1", "view2", "view3"],
            0
        )
        self.assertEqual(
            render_to_content(widget, (15,)),
            render_widgets_to_content([
                urwid.AttrMap(urwid.Text("view1"), "tabs focus"),
                urwid.AttrMap(urwid.Text("view2"), "tabs"),
                urwid.AttrMap(urwid.Text("view3"), "tabs")
            ], (15,), inline=True)
        )

if __name__ == "__main__":
    unittest.main()
