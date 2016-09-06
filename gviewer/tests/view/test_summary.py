import unittest
import urwid
import mock

from ..util import render_to_content, render_widgets_to_content
from gviewer.view.summary import (
    SummaryItemWidget, SummaryListWalker,
    FilterSummaryListWalker, SummaryListWidget)
from gviewer.view.summary import _verify_keys
from gviewer.view.detail import DetailWidget
from gviewer.view.element import View
from gviewer.action import Actions
from gviewer.store import StaticDataStore
from gviewer.context import DisplayerContext
from gviewer.config import Config
from gviewer.displayer import BaseDisplayer


class TestSummaryItemWidget(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.controller.open_view = mock.Mock(side_effect=self._open_view)

        self.context = mock.Mock()
        self.context.config.keys = dict()

        self.action_a = mock.Mock()
        self.displayer_context = DisplayerContext(
            None, self, Actions([("a", "aaaa", self.action_a)]))

        self.widget = SummaryItemWidget(
            "message", "summary", self.displayer_context, controller=self.controller,
            context=self.context)

        self.new_widget = None

    def get_views(self):
        return [("view", self.view1)]

    def view1(self, message):
        return View([])

    def _open_view(self, widget, **kwargs):
        self.new_widget = widget

    def test_render(self):
        self.assertEqual(
            render_to_content(self.widget, (7,)),
            render_widgets_to_content(
                [urwid.AttrMap(urwid.Text("summary"), "summary")],
                (7, 1))
        )

    def test_keypress_enter(self):
        self.assertIsNone(self.widget.keypress(None, "enter"))
        self.assertIsNotNone(self.new_widget)
        self.assertIsInstance(self.new_widget, DetailWidget)

    def test_keypress_custom_action(self):
        self.assertIsNone(self.widget.keypress(None, "a"))
        self.action_a.assert_called_with(self.controller, "message", self.widget)

    def test_set_title(self):
        self.widget.set_title("hahaha")
        self.assertEqual(self.widget.get_title_as_plain_text(), "hahaha")


class TestSummaryListWalker(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.controller.open_error = mock.Mock(
            side_effect=self._open_error)

        self.context = mock.Mock()
        self.context.config.keys = dict()

        self.displayer_context = mock.Mock()
        self.displayer_context.displayer.summary = mock.Mock(
            side_effect=lambda m: m)
        self.displayer_context.displayer.match = mock.Mock(
            side_effect=lambda k, m, s: k in s)
        self.on_receive = mock.Mock()

        self.error = False

        self.walker = SummaryListWalker(
            controller=self.controller, context=self.context,
            displayer_context=self.displayer_context,
            on_receive=self.on_receive)

    def _open_error(self, *args, **kwargs):
        self.error = True

    def test_msg_listener_register(self):
        self.displayer_context.store.register.assert_called_once_with(
            self.walker)

    def test_recv(self):
        self.displayer_context.displayer.summary = mock.Mock(return_value="message")

        self.walker.recv("new message")
        self.assertEqual(len(self.walker), 1)
        self.assertFalse(self.error)

        self.displayer_context.displayer.summary.assert_called_once_with("new message")

    def test_recv_failed(self):
        self.displayer_context.displayer.summary = mock.Mock(
            side_effect=ValueError("failed"))

        self.walker.recv("new message")
        self.assertEqual(len(self.walker), 0)
        self.assertTrue(self.error)


class TestFilterSummaryListWalker(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.controller.open_error = mock.Mock(
            side_effect=self._open_error)

        self.context = mock.Mock()
        self.context.config.keys = dict()

        self.displayer_context = mock.Mock()
        self.displayer_context.displayer = BaseDisplayer()
        self.on_receive = mock.Mock()
        self.error = False

        self.original_walker = SummaryListWalker(
            content=[
                SummaryItemWidget(
                    "message 1", "summary 1",
                    self.displayer_context,
                    controller=self.controller,
                    context=self.context),
                SummaryItemWidget(
                    "message 2", "summary 2",
                    self.displayer_context,
                    controller=self.controller,
                    context=self.context)
            ],
            controller=self.controller,
            context=self.context,
            displayer_context=self.displayer_context,
            on_receive=self.on_receive
        )

    def _open_error(self, *args, **kwargs):
        self.error = True

    def test_construct(self):
        walker = FilterSummaryListWalker(
            self.original_walker, "summary 1")
        self.assertEqual(len(walker), 1)

    def test_recv_with_match(self):
        walker = FilterSummaryListWalker(
            self.original_walker, "summary 1")
        walker.recv("summary 1111")
        self.assertEqual(len(walker), 2)

    def test_recv_with_not_match(self):
        walker = FilterSummaryListWalker(
            self.original_walker, "summary 1")
        walker.recv("summary")
        self.assertEqual(len(walker), 1)

    def test_recv_failed(self):
        self.displayer_context.displayer.summary = mock.Mock(side_effect=ValueError("failed"))

        walker = FilterSummaryListWalker(
            self.original_walker, "summary 1")

        walker.recv("summary 1")
        self.assertEqual(len(walker), 1)
        self.assertTrue(self.error)

    def test_close(self):
        walker = FilterSummaryListWalker(
            self.original_walker, "summary 1")
        walker.close()
        self.displayer_context.store.unregister.assert_called_once_with(walker)


class TestSummaryListWidget(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()

        self.displayer_context = DisplayerContext(
            StaticDataStore(["summary 1", "summary 2"]),
            BaseDisplayer())

        self.context = mock.Mock()
        self.context.config = Config()

        self.widget = SummaryListWidget(
            self.displayer_context,
            controller=self.controller,
            context=self.context)

        self.displayer_context.store.setup()

    def test_render(self):
        self.assertEqual(
            render_to_content(self.widget, (9, 2)),
            render_widgets_to_content([
                urwid.AttrMap(urwid.Text("summary 1"), "summary"),
                urwid.AttrMap(urwid.Text("summary 2"), "summary")
            ], (9, 2))
        )

    def test_open_search(self):
        self.widget._open_search()
        self.controller.open_edit.assert_called_with(self.widget.search_widget)

    def test_filter(self):
        self.widget._filter("summary 1")
        self.assertIsInstance(self.widget.current_walker, FilterSummaryListWalker)
        self.assertEqual(len(self.widget.current_walker), 1)

    def test_filter_with_empty(self):
        self.widget._filter("")
        self.assertIs(
            self.widget.current_walker,
            self.widget.base_walker)

    def test_keypress_open_search(self):
        self.widget.keypress(None, "/")
        self.controller.open_edit.assert_called_with(self.widget.search_widget)

    def test_keypress_clear_search(self):
        self.widget._filter("test")
        self.assertEqual(len(self.widget.current_walker), 0)

        self.widget.keypress((0,), "q")
        self.assertIs(
            self.widget.current_walker,
            self.widget.base_walker)
        self.assertEqual(len(self.widget.current_walker), 2)

    def test_keypress_back(self):
        self.widget.keypress((0,), "q")
        self.controller.back.assert_called_with()

    def test_keypress_open_help(self):
        self.assertIsNone(self.widget.keypress((0, 0), "?"))
        self.controller.open_view.assert_called_with(self.widget.help_widget)

    def test_keypress_bottom_and_top(self):
        self.widget.keypress((10, 10), "G")
        self.assertEqual(self.widget._w.focus_position, 1)
        self.controller._update_info.assert_called_with("[2/2]")

        self.widget.keypress((10, 10), "g")
        self.assertEqual(self.widget._w.focus_position, 0)
        self.controller._update_info.assert_called_with("[1/2]")

    def test_keypress_bottom_and_top_when_search(self):
        self.widget._filter("summary")
        self.widget.keypress((10, 10), "G")
        self.assertEqual(self.widget._w.focus_position, 1)
        self.widget.keypress((10, 10), "g")
        self.assertEqual(self.widget._w.focus_position, 0)

    def test_keypress_clear_item(self):
        self.widget.keypress((10, 10), "x")
        self.assertEqual(len(self.widget.current_walker), 1)
        self.controller._update_info.assert_called_with("[1/1]")

    def test_keypress_clear_items(self):
        self.widget.keypress((10, 10), "X")
        self.assertEqual(len(self.widget.current_walker), 0)
        self.controller._update_info.assert_called_with("[0/0]")

    def test_keypress_up_and_down(self):
        self.widget.keypress((10, 10), "down")
        self.assertEqual(self.widget._w.focus_position, 1)
        self.controller._update_info.assert_called_with("[2/2]")

        self.widget.keypress((10, 10), "up")
        self.assertEqual(self.widget._w.focus_position, 0)
        self.controller._update_info.assert_called_with("[1/2]")

    def test_auto_scroll(self):
        displayer_context = DisplayerContext(
            StaticDataStore(["summary 1", "summary 2"]),
            BaseDisplayer())
        self.context.config = Config(auto_scroll=True)
        widget = SummaryListWidget(
            displayer_context,
            controller=self.controller,
            context=self.context)
        displayer_context.store.setup()

        self.assertEqual(widget._w.focus_position, 1)
        widget.current_walker.recv("summary 3")
        self.assertEqual(widget._w.focus_position, 2)

        widget._w.set_focus(0)
        widget.current_walker.recv("summary 4")
        self.assertEqual(widget._w.focus_position, 0)


class TestSummary(unittest.TestCase):
    def test_verify_keys(self):
        _verify_keys(Actions([("p", "pppp", None)]))

    def test_verify_keys_failed(self):
        with self.assertRaises(ValueError):
            _verify_keys(Actions([("/", "search", None)]))
