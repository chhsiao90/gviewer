import unittest
import urwid
import sys

from util import render_to_content, render_widgets_to_content
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


class FooterTest(unittest.TestCase):
    def test_render(self):
        widget = Footer(None)
        self.assertEqual(
            render_to_content(widget, (20, 2)),
            render_widgets_to_content(
                [Helper(), Notification(None)],
                (20, 2))
        )


if __name__ == "__main__":
    unittest.main()
