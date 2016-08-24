import unittest
import urwid
import sys

try:
    import unittest.mock as mock
except:
    import mock

from util import render_to_content, render_widgets_to_content, render_to_text
from gviewer.parent import ParentFrame, Footer, Helper, Notification
from gviewer.config import Config
from gviewer.summary import SummaryListWidget
from gviewer.view import ViewWidget
from gviewer.error import ErrorWidget
from gviewer import Line, Group, Groups, StaticDataStore


class ParentFrameTest(unittest.TestCase):
    def setUp(self):
        self.messages = [
            ["aaa1", "aaa2", "aaa3"],
            ["bbb1", "bbb2", "bbb3"],
            ["ccc1", "ccc2", "ccc3"]
        ]

        self.data_store = StaticDataStore(self.messages)

        self.widget = ParentFrame(
            self.data_store,
            self,
            Config()
        )
        self.data_store.set_up()

    def summary(self, message):
        return ";".join(message)

    def get_views(self):
        return [
            ("view1", self.view),
            ("view2", self.view)
        ]

    def view(self, message):
        return Groups([Group("foo", [Line(m) for m in message])])

    def test_render(self):
        self.assertEqual(
            render_to_content(self.widget, (30, 10)),
            render_widgets_to_content([
                urwid.AttrMap(urwid.Text("General Viewer"), "header"),
                urwid.AttrMap(urwid.Text(";".join(self.messages[0])), "summary"),
                urwid.AttrMap(urwid.Text(";".join(self.messages[1])), "summary"),
                urwid.AttrMap(urwid.Text(";".join(self.messages[2])), "summary"),
                urwid.Text(""),
                urwid.Text(""),
                urwid.Text(""),
                urwid.Text(""),
                Footer(self)
            ], (30, 10))
        )

    def test_initial_with_summary(self):
        self.assertIs(
            self.widget.contents["body"][0],
            self.widget.summary
        )
        self.assertIsInstance(
            self.widget.summary,
            SummaryListWidget
        )

    def test_display_view(self):
        self.widget.display_view(self.messages[0], 0)
        self.assertIsInstance(
            self.widget.contents["body"][0],
            ViewWidget
        )

    def test_open_summary(self):
        self.widget.display_view(self.messages[0], 0)
        self.widget.open_summary()
        self.assertIs(
            self.widget.contents["body"][0],
            self.widget.summary
        )
        self.assertIsInstance(
            self.widget.summary,
            SummaryListWidget
        )

    def test_open_error(self):
        try:
            raise ValueError("error")
        except:
            exc_info = sys.exc_info()
        self.widget.open_error(exc_info)
        self.assertIsInstance(
            self.widget.contents["body"][0],
            ErrorWidget
        )

    def test_notify(self):
        self.widget.notify("test")
        self.assertEqual(
            self.widget.focus_position,
            "footer")
        self.assertEqual(
            self.widget.footer._w.focus_position, 1)
        self.assertEqual(
            render_to_text(self.widget.footer.notification, (5,)),
            ["test "])


class FooterTest(unittest.TestCase):
    def test_render(self):
        widget = Footer(None)
        self.assertEqual(
            render_to_content(widget, (20, 2)),
            render_widgets_to_content(
                [Helper(), Notification(None)],
                (20, 2)))

    def test_notify(self):
        widget = Footer(None)
        widget.notify("test")
        self.assertEqual(
            render_to_text(widget.notification, (5,)),
            ["test "])


class NotificationTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()
        self.widget = Notification(
            self.parent)

    def test_render_default(self):
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["     "])

    def test_render_notify(self):
        self.widget.notify("test")
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["test "])

    def test_exit_from_notify(self):
        self.widget.notify("test")
        self.widget.keypress((0, 0), "a")  # any keys

        self.parent.exit_notify.assert_called_with()
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["     "])

    def test_exit_with_q(self):
        self.assertIsNone(
            self.widget.keypress((0, 0), "q"))


if __name__ == "__main__":
    unittest.main()
