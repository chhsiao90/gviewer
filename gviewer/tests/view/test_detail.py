import unittest
import urwid
import mock

from gviewer.tests.util import render_to_content, render_widgets_to_content
from gviewer.view.detail import DetailWidget, Tabs
from gviewer.view.detail import _verify_keys
from gviewer.view.element import View, Text, Group
from gviewer.action import Actions


class DetailWidgetTest(unittest.TestCase):
    def setUp(self):
        self.displayer_context = mock.Mock()

        self.displayer_context.displayer.get_views = mock.Mock(return_value=[
            ("View 1", self._view1),
            ("View 2", self._view2),
            ("View 3", self._view3)
        ])

        self.context = mock.Mock()
        self.context.config.keys = dict()
        self.controller = mock.Mock()
        self.controller.open_view = mock.Mock(side_effect=self._open_view)

        self.test_message = dict(view1="view1", view2="view2", view3="view3")

        self.widget = DetailWidget(
            self.test_message, self.displayer_context,
            index=0, controller=self.controller, context=self.context)
        self.new_widget = None

    def _view1(self, message):
        return self._display(message["view1"])

    def _view2(self, message):
        return self._display(message["view2"])

    def _view3(self, message):
        return self._display(message["view3"])

    def _display(self, message):
        return View([Group("Title", [Text(message)])])

    def _open_view(self, widget, push_prev):
        self.new_widget = widget

    def test_render(self):
        self.assertEqual(
            render_to_content(self.widget._w.contents["body"][0], (7, 2)),
            render_widgets_to_content([
                urwid.AttrMap(urwid.Text("Title"), "view-title"),
                urwid.AttrMap(urwid.Text("view1"), "view-item")
            ], (7, 2))
        )

    def test_next_view(self):
        self.widget.keypress((0,), "tab")
        self.assertIsNotNone(self.new_widget)
        self.assertEqual(self.new_widget.index, 1)

        self.widget = self.new_widget
        self.widget.keypress((0,), "tab")
        self.assertIsNot(self.new_widget, self.widget)
        self.assertEqual(self.new_widget.index, 2)

        self.widget = self.new_widget
        self.widget.keypress((0,), "tab")
        self.assertIsNot(self.new_widget, self.widget)
        self.assertEqual(self.new_widget.index, 0)

    def test_prev_view(self):
        self.widget.keypress((0,), "shift tab")
        self.assertIsNotNone(self.new_widget)
        self.assertEqual(self.new_widget.index, 2)

        self.widget = self.new_widget
        self.widget.keypress((0,), "shift tab")
        self.assertIsNot(self.new_widget, self.widget)
        self.assertEqual(self.new_widget.index, 1)

        self.widget = self.new_widget
        self.widget.keypress((0,), "shift tab")
        self.assertIsNot(self.new_widget, self.widget)
        self.assertEqual(self.new_widget.index, 0)

    def test_no_tab(self):
        self.displayer_context.displayer.get_views = mock.Mock(return_value=[
            ("View 1", lambda m: self._display(m["view1"]))
        ])
        self.widget = DetailWidget(
            self.test_message, self.displayer_context,
            index=0, controller=self.controller, context=self.context)

        with self.assertRaises(KeyError):
            self.widget._w.contents["header"]

    def test_swtich_tab_when_no_tab(self):
        self.displayer_context.displayer.get_views = mock.Mock(return_value=[
            ("View 1", lambda m: self._display(m["view1"]))
        ])
        self.widget = DetailWidget(
            self.test_message, self.displayer_context,
            index=0, controller=self.controller, context=self.context)

        self.widget.keypress((0,), "tab")
        self.assertIsNone(self.new_widget)

        self.widget.keypress((0,), "shift tab")
        self.assertIsNone(self.new_widget)

    def test_open_search(self):
        self.widget.keypress((0,), "/")
        self.assertEqual(
            self.widget.body.contents[1][0],
            self.widget.search_widget)
        self.assertIs(self.widget.body.focus, self.widget.search_widget)

    def test_close_search(self):
        self.assertEqual(len(self.widget.body.contents), 1)
        self.widget._close_search()
        self.assertEqual(len(self.widget.body.contents), 1)
        self.widget._open_search()
        self.assertEqual(len(self.widget.body.contents), 2)
        self.widget._close_search()
        self.assertEqual(len(self.widget.body.contents), 1)

    def test_clear_search(self):
        self.assertEqual(len(self.widget.body.contents), 1)
        self.widget._open_search()
        self.assertEqual(len(self.widget.body.contents), 2)
        self.widget._clear_search()
        self.assertEqual(len(self.widget.body.contents), 1)

    def test_open_summary(self):
        self.widget.keypress((0,), "q")
        self.controller.back.assert_called_with()

    def test_search(self):
        self.widget.search_widget.keypress((4,), "v")
        self.widget.search_widget.keypress((4,), "i")
        self.widget.search_widget.keypress((4,), "e")
        self.widget.search_widget.keypress((4,), "w")
        self.widget.search_widget.keypress((4,), "enter")

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
            render_to_content(self.widget.content_widget, (5, 3)),
            match)

        self.widget.keypress((0,), "n")
        self.assertEqual(
            render_to_content(self.widget.content_widget, (5, 3)),
            no_match)

        self.widget.keypress((0,), "N")
        self.assertEqual(
            render_to_content(self.widget.content_widget, (5, 3)),
            match)

        self.widget.keypress((0,), "N")
        self.assertEqual(
            render_to_content(self.widget.content_widget, (5, 3)),
            no_match)

    def test_editing(self):
        self.widget._open_search()
        self.assertTrue(self.widget.is_editing())

        keypress_result = self.widget.keypress((0, 0), "a")
        self.assertEqual(keypress_result, "a")
        keypress_result = self.widget.keypress((0, 0), "q")
        self.assertEqual(keypress_result, "q")


class TabsTest(unittest.TestCase):
    def test_render(self):
        widget = Tabs(["view1", "view2", "view3"], 0)
        self.assertEqual(
            render_to_content(widget, (15,)),
            render_widgets_to_content([
                urwid.AttrMap(urwid.Text("view1"), "tabs focus"),
                urwid.AttrMap(urwid.Text("view2"), "tabs"),
                urwid.AttrMap(urwid.Text("view3"), "tabs")
            ], (15,), inline=True)
        )


class TestDetail(unittest.TestCase):
    def test_verify_keys(self):
        _verify_keys(Actions([("p", "pppp", None)]))

    def test_verify_keys_failed(self):
        with self.assertRaises(ValueError):
            _verify_keys(Actions([("/", "search", None)]))
