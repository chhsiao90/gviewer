import unittest
import urwid

try:
    import unittest.mock as mock
except:
    import mock

from util import render_to_content, render_widgets_to_content
from gviewer.summary import SummaryItemWidget, SummaryListWalker, FilterSummaryListWalker, SummaryListWidget
from gviewer.action import Actions


class SummaryItemWidgetTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()
        self.parent.config.keys = dict()

        self.context = mock.Mock()

    def test_render(self):
        widget = SummaryItemWidget(
            self.parent,
            self.context,
            None,
            "summary"
        )
        self.assertEqual(
            render_to_content(widget, (7,)),
            render_widgets_to_content(
                [urwid.AttrMap(urwid.Text("summary"), "summary")],
                (7, 1))
        )

    def test_keypress_enter(self):
        widget = SummaryItemWidget(
            self.parent,
            self.context,
            "message",
            "summary"
        )
        self.assertIsNone(widget.keypress(None, "enter"))
        self.parent.display_view.assert_called_with(
            "message", 0)


class SummaryListWalkerTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()
        self.parent.open_error = mock.Mock(
            side_effect=self._open_error)

        self.context = mock.Mock()
        self.context.config.keys = dict()

        self.error = False

        self.walker = SummaryListWalker(
            self.parent, self.context)

    def _open_error(self, *args, **kwargs):
        self.error = True

    def test_msg_listener_register(self):
        self.parent.msg_listener.register.assert_called_once_with(
            self.walker)

    def test_recv(self):
        self.context.displayer.summary = mock.Mock(return_value="message")

        self.walker.recv("new message")
        self.assertEqual(len(self.walker), 1)
        self.assertFalse(self.error)

        self.context.displayer.summary.assert_called_once_with("new message")

    def test_recv_failed(self):
        self.context.displayer.summary = mock.Mock(
            side_effect=ValueError("failed"))

        self.walker.recv("new message")
        self.assertEqual(len(self.walker), 0)
        self.assertTrue(self.error)


class FilterSummaryListWalkerTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()
        self.parent.open_error = mock.Mock(
            side_effect=self._open_error)
        self.parent.config.keys = dict()

        self.context = mock.Mock()
        self.context.displayer.match = mock.Mock(
            side_effect=lambda k, m, s: k in s)
        self.context.displayer.summary = mock.Mock(
            side_effect=lambda m: m)

        self.error = False

        self.origin_walker = SummaryListWalker(
            self.parent,
            self.context,
            content=[
                SummaryItemWidget(self.parent, self.context, "message 1", "summary 1"),
                SummaryItemWidget(self.parent, self.context, "message 2", "summary 2")
            ]
        )

    def _open_error(self, *args, **kwargs):
        self.error = True

    def test_construct(self):
        walker = FilterSummaryListWalker(
            self.origin_walker, "summary 1")
        self.assertEqual(len(walker), 1)

        self.context.displayer.match.assert_any_call(
            "summary 1", "message 1", "summary 1")
        self.context.displayer.match.assert_any_call(
            "summary 1", "message 2", "summary 2")

    def test_recv_with_match(self):
        walker = FilterSummaryListWalker(
            self.origin_walker, "summary 1")
        walker.recv("summary 1111")
        self.assertEqual(len(walker), 2)

    def test_recv_with_not_match(self):
        walker = FilterSummaryListWalker(
            self.origin_walker, "summary 1")
        walker.recv("summary")
        self.assertEqual(len(walker), 1)

    def test_recv_failed(self):
        self.context.displayer.summary.side_effect = ValueError("failed")

        walker = FilterSummaryListWalker(
            self.origin_walker, "summary 1")

        walker.recv("summary 1")
        self.assertEqual(len(walker), 1)
        self.assertTrue(self.error)

    def test_close(self):
        walker = FilterSummaryListWalker(
            self.origin_walker, "summary 1")
        walker.close()
        self.parent.msg_listener.unregister.assert_called_once_with(walker)


class SummaryListWidgetTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()

        self.context = mock.Mock()
        self.context.config.keys = dict()
        self.context.summary_actions = Actions()
        self.context.displayer.match = mock.Mock(
            side_effect=lambda k, m, s: k in s)

        self.walker = SummaryListWalker(
            self.parent,
            self.context,
            content=[
                SummaryItemWidget(self.parent, self.context, "message 1", "summary 1"),
                SummaryItemWidget(self.parent, self.context, "message 2", "summary 2")
            ]
        )

        self.widget = SummaryListWidget(
            self.walker,
            self.parent,
            self.context
        )

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

        self.assertIs(self.widget._w.focus, self.widget.search_widget)
        self.assertTrue(self.widget.is_editing())

        self.assertIs(
            self.widget._w.contents[1][0],
            self.widget.search_widget
        )

    def test_close_search(self):
        self.widget._close_search()  # nothing happen
        self.assertFalse(self.widget.is_editing())

        self.widget._open_search()
        self.assertTrue(self.widget.is_editing())

        self.widget._close_search()
        self.assertFalse(self.widget.is_editing())
        self.assertEqual(len(self.widget._w.contents), 1)

    def test_filter(self):
        self.widget._filter("summary 1")
        self.assertIsInstance(self.widget._w.focus, urwid.ListBox)
        self.assertIsInstance(self.widget.current_walker, FilterSummaryListWalker)
        self.assertEqual(len(self.widget.current_walker), 1)

    def test_filter_with_empty(self):
        self.widget._filter("")
        self.assertIs(
            self.widget.current_walker,
            self.widget.base_walker)

    def test_keypress_on_editing(self):
        self.widget._open_search()
        self.assertIsNone(self.widget.keypress((0,), "q"))
        self.assertIsNone(self.widget.keypress((0,), "j"))
        self.assertIsNone(self.widget.keypress((0,), "/"))
        self.assertEqual(
            self.widget.search_widget.get_keyword(),
            "qj/")

    def test_keypress_open_search(self):
        self.widget.keypress(None, "/")
        self.assertTrue(self.widget.is_editing())

    def test_keypress_clear_search(self):
        self.widget._filter("test")
        self.assertEqual(len(self.widget.current_walker), 0)

        self.widget.keypress((0,), "q")
        self.assertIs(
            self.widget.current_walker,
            self.widget.base_walker)
        self.assertEqual(len(self.widget.current_walker), 2)


if __name__ == "__main__":
    unittest.main()
