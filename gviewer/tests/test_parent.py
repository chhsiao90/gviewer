import unittest
import urwid

from .util import render_to_content, render_widgets_to_content, render_to_text
from gviewer.parent import ParentFrame, Footer, Helper, Notification
from gviewer.config import Config
from gviewer.context import Context, DisplayerContext
from gviewer.view.error import ErrorWidget
from gviewer.view.element import View, Text, Group
from gviewer.view.summary import SummaryListWidget
from gviewer.store import StaticDataStore


class ParentFrameTest(unittest.TestCase):
    def setUp(self):
        self.messages = [
            ["aaa1", "aaa2", "aaa3"],
            ["bbb1", "bbb2", "bbb3"],
            ["ccc1", "ccc2", "ccc3"]
        ]
        store = StaticDataStore(self.messages)
        main_context = DisplayerContext(store, self)

        messages2 = [
            ["ddd1", "ddd2", "ddd3"],
            ["eee1", "eee2", "eee3"],
            ["fff1", "fff2", "fff3"]
        ]
        store2 = StaticDataStore(messages2)
        self.other_context = DisplayerContext(store2, self)

        context = Context(
            Config(), main_context=main_context,
            other_contexts=[self.other_context])
        self.widget = ParentFrame(context)

        store.setup()

    def summary(self, message):
        return ";".join(message)

    def get_views(self):
        return [
            ("view1", self.view),
            ("view2", self.view)
        ]

    def view(self, message):
        return View([Group("foo", [Text(m) for m in message])])

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
                Footer()
            ], (30, 10))
        )

    def test_initial_with_main(self):
        self.assertIs(
            self.widget.contents["body"][0],
            self.widget.main
        )

    def test_back(self):
        self.widget.open_view(urwid.Text(""))
        self.widget.back()
        self.assertIs(
            self.widget.contents["body"][0],
            self.widget.main
        )

    def test_back_to_exit(self):
        with self.assertRaises(urwid.ExitMainLoop):
            self.widget.back()

    def test_open_error(self):
        try:
            raise ValueError("error")
        except:
            self.widget.open_error()

        self.assertIsInstance(
            self.widget.contents["body"][0],
            ErrorWidget
        )

    def test_notify(self):
        self.widget.notify("test")

        self.assertEqual(
            render_to_text(self.widget.footer.notification, (5,)),
            ["test "])

    def test_run_before_keypress(self):
        self.widget.notify("test")
        self.widget.run_before_keypress()
        self.assertEqual(
            render_to_text(self.widget.footer.notification, (5,)),
            ["     "])

    def test_open_view(self):
        open_view = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        self.widget.open_view(open_view)

        self.assertIs(self.widget.contents["body"][0], open_view)
        self.assertEqual(len(self.widget.histories), 1)
        self.assertIs(self.widget.histories[0], self.widget.main)

    def test_open_same_view_twice(self):
        open_view = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        self.widget.open_view(open_view)

        self.assertIs(self.widget.contents["body"][0], open_view)

        self.widget.open_view(open_view)
        self.assertEqual(len(self.widget.histories), 1)

    def test_open_view_by_context(self):
        self.assertEqual(len(self.widget.others), 1)
        other_widget = self.widget.others[self.other_context]
        self.assertIsInstance(other_widget, SummaryListWidget)

        self.widget.open_view_by_context(self.other_context)
        self.assertIs(
            self.widget.contents["body"][0], other_widget)
        self.assertEqual(len(self.widget.histories), 1)
        self.assertIs(self.widget.histories[0], self.widget.main)

    def test_open_view_by_context_failed(self):
        self.widget.open_view_by_context(DisplayerContext(None, None))
        self.assertIsInstance(
            self.widget.contents["body"][0], ErrorWidget)
        self.assertEqual(len(self.widget.histories), 1)
        self.assertIs(self.widget.histories[0], self.widget.main)


class FooterTest(unittest.TestCase):
    def test_render(self):
        widget = Footer()
        self.assertEqual(
            render_to_content(widget, (20, 2)),
            render_widgets_to_content(
                [Helper(), Notification()],
                (20, 2)))

    def test_notify(self):
        widget = Footer()
        widget.notify("test")
        self.assertEqual(
            render_to_text(widget.notification, (5,)),
            ["test "])


class NotificationTest(unittest.TestCase):
    def setUp(self):
        self.widget = Notification()

    def test_render_default(self):
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["     "])

    def test_render_notify(self):
        self.widget.notify("test")
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["test "])
