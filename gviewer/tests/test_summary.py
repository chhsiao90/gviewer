import unittest
import urwid

try:
    import unittest.mock as mock
except:
    import mock

from util import render_to_content, render_widgets_to_content
from gviewer.summary import SummaryItemWidget, SummaryListWalker, FilterSummaryListWalker


class SummaryItemWidgetTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()
        self.parent.display_view = mock.Mock()

    def test_render(self):
        widget = SummaryItemWidget(
            self.parent,
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
            "message",
            "summary"
        )
        self.assertEqual(
            widget.keypress(None, "enter"),
            None
        )
        self.parent.display_view.assert_called_with(
            "message", 0)


class SummaryListWalkerTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()

        self.parent.displayer = mock.Mock()
        self.parent.displayer.summary = mock.Mock()

        self.parent.msg_listener = mock.Mock()
        self.parent.msg_listener.register = mock.Mock()

        self.error = False
        self.parent.open_error = mock.Mock(
            side_effect=self._open_error)

        self.widget = SummaryListWalker(
            self.parent)

    def _open_error(self, *args, **kwargs):
        self.error = True

    def test_msg_listener_register(self):
        self.parent.msg_listener.register.assert_called_once_with(
            self.widget)

    def test_recv(self):
        self.parent.displayer.summary.return_value = "message"

        self.widget.recv("new message")
        self.assertEqual(len(self.widget), 1)
        self.assertFalse(self.error)

        self.parent.displayer.summary.assert_called_once_with("new message")

    def test_recv_failed(self):
        self.parent.display_view.summary.side_effect = ValueError("failed")

        self.widget.recv("new message")
        self.assertEqual(len(self.widget), 0)
        self.assertTrue(self.error)


class FilterSummaryListWalkerTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()

        self.parent.displayer = mock.Mock()
        self.parent.displayer.match = mock.Mock(
            side_effect=self._match)
        self.parent.displayer.summary = mock.Mock()

        self.parent.msg_listener = mock.Mock()
        self.parent.msg_listener.register = mock.Mock()

        self.error = False
        self.parent.open_error = mock.Mock(
            side_effect=self._open_error)

        self.origin_walker = SummaryListWalker(
            self.parent,
            content=[
                SummaryItemWidget(self.parent, "message 1", "summary 1"),
                SummaryItemWidget(self.parent, "message 2", "summary 2")
            ]
        )

    def _match(self, search, message, summary):
        return search in summary

    def _open_error(self, *args, **kwargs):
        self.error = True

    def test_construct(self):
        widget = FilterSummaryListWalker(
            self.origin_walker, "summary 1")
        self.assertEqual(len(widget), 1)

        self.parent.displayer.match.assert_any_call(
            "summary 1", "message 1", "summary 1")
        self.parent.displayer.match.assert_any_call(
            "summary 1", "message 2", "summary 2")


if __name__ == "__main__":
    unittest.main()
