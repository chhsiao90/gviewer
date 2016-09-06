import unittest
import mock

from gviewer.controller import Controller


class ControllerTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()
        self.controller = Controller(self.parent)

    def test_open_view(self):
        self.controller.open_view("widget")
        self.parent.open_view.assert_called_with("widget", push_prev=True)

        self.controller.open_view("widget", push_prev=False)
        self.parent.open_view.assert_called_with("widget", push_prev=False)

    def test_open_view_by_context(self):
        self.controller.open_view_by_context("context")
        self.parent.open_view_by_context.assert_called_with("context")

    def test_notify(self):
        self.controller.notify("message")
        self.parent.notify.assert_called_with("message")

    def test_open_error(self):
        self.controller.open_error()
        self.parent.open_error.assert_called_with()

    def test_back(self):
        self.controller.back()
        self.parent.back.assert_called_with()

    def test_run_before_keypress(self):
        self.controller._run_before_keypress()
        self.parent.run_before_keypress.assert_called_with()
