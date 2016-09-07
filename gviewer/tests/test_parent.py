import unittest
import urwid
import mock

from .util import render_to_content, render_widgets_to_content, render_to_text
from gviewer.parent import ParentFrame, Footer, Helper, Notification
from gviewer.config import Config
from gviewer.context import Context, DisplayerContext
from gviewer.basic_widget import BasicWidget
from gviewer.view.error import ErrorWidget
from gviewer.view.element import View, Text, Group
from gviewer.view.summary import SummaryListWidget
from gviewer.store import StaticDataStore


class TestParentFrame(unittest.TestCase):
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
                Footer(helper=Helper(info_widget=urwid.Text("[1/3]")))
            ], (30, 10))
        )

    def test_initial_with_main(self):
        self.assertIs(
            self.widget.contents["body"][0],
            self.widget.main
        )

    def test_back(self):
        self.widget.open_view(BasicWidget(widget=urwid.Text("")))
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

    def test_open_edit(self):
        self.widget.open_edit(urwid.Edit("/"))
        self.assertEqual(self.widget.focus_position, "footer")
        self.assertEqual(
            render_to_text(self.widget.footer.notification, (5,)), ["/    "])

    def test_close_edit(self):
        self.widget.open_edit(urwid.Edit("/"))
        self.widget.close_edit()
        self.assertEqual(
            render_to_text(self.widget.footer.notification, (5,)), ["     "])

    def test_run_before_keypress(self):
        self.widget.notify("test")
        self.widget.run_before_keypress()
        self.assertEqual(
            render_to_text(self.widget.footer.notification, (5,)),
            ["     "])

    def test_open_view(self):
        open_view = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        open_view = BasicWidget(widget=open_view)
        self.widget.open_view(open_view)

        self.assertIs(self.widget.contents["body"][0], open_view)
        self.assertEqual(len(self.widget.histories), 1)
        self.assertIs(self.widget.histories[0], self.widget.main)

    def test_open_same_view_twice(self):
        open_view = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        open_view = BasicWidget(widget=open_view)
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

    def test_update_info(self):
        self.widget.update_info(
            self.widget.contents["body"][0], "test")
        self.assertEqual(
            self.widget.contents["footer"][0].helper.info_widget.text,
            "test")

        self.widget.update_info(
            urwid.Text("test"), "not update")
        self.assertEqual(
            self.widget.contents["footer"][0].helper.info_widget.text,
            "test")


class TestFooter(unittest.TestCase):
    def setUp(self):
        self.helper = mock.Mock()
        self.notification = mock.Mock()
        self.widget = Footer(helper=self.helper, notification=self.notification)

    def test_render(self):
        widget = Footer()
        self.assertEqual(
            render_to_content(widget, (20, 2)),
            render_widgets_to_content(
                [Helper(), Notification()],
                (20, 2)))

    def test_notify(self):
        self.widget.notify("test")
        self.notification.notify.assert_called_with("test")

    def test_clear_notify(self):
        self.widget.clear_notify()
        self.notification.clear.assert_called_with()

    def test_open_edit(self):
        w = urwid.Edit()
        self.widget.open_edit(w)
        self.notification.open_edit.assert_called_with(w)

    def test_close_edit(self):
        self.widget.close_edit()
        self.notification.close_edit.assert_called_with()


class TestNotification(unittest.TestCase):
    def setUp(self):
        self.widget = Notification()

    def test_render_default(self):
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["     "])

    def test_notify(self):
        self.widget.notify("test")
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["test "])

    def test_clear_notify(self):
        self.widget.notify("test")
        self.widget.clear()
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["     "])

    def test_open_edit(self):
        w = urwid.Edit("/")
        self.widget.open_edit(w)

        self.assertIs(self.widget._edit_widget, w)
        self.assertTrue(self.widget.is_editing())
        self.assertEqual(
            render_to_text(self.widget, (5,)),
            ["/    "])

    def test_notify_on_edit(self):
        self.widget.open_edit(urwid.Edit("/"))
        self.widget.notify("hahaha")

        self.assertEqual(
            render_to_text(self.widget, (6,)),
            ["hahaha"])

        self.widget.clear()
        self.assertEqual(
            render_to_text(self.widget, (6,)),
            ["/     "])

    def test_close_edit(self):
        self.widget.open_edit(urwid.Edit("/"))
        self.widget.close_edit()
        self.assertFalse(self.widget.is_editing())
        self.assertIsNone(self.widget._edit_widget)
