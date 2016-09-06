import unittest
import mock

from ..util import render_to_content
from gviewer.view.error import ErrorWidget


class ErrorWidgetTest(unittest.TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.context = mock.Mock()

    def test_render(self):
        try:
            raise ValueError("wrong value")
        except:
            widget = ErrorWidget(
                controller=self.controller,
                context=self.context
            )

        contents = render_to_content(widget, (200, 4))
        self.assertEqual(len(contents), 4)

        self.assertEqual(contents[0][0][0], "error")
        self.assertEqual(contents[0][0][2].rstrip(), "Traceback (most recent call last):")

        self.assertEqual(contents[1][0][0], "error")
        self.assertTrue("test_error.py" in contents[1][0][2])
        self.assertTrue("test_render" in contents[1][0][2])

        self.assertEqual(contents[2][0][0], "error")
        self.assertEqual(contents[2][0][2].strip(), "raise ValueError(\"wrong value\")")

        self.assertEqual(contents[3][0][0], "error")
        self.assertEqual(contents[3][0][2].strip(), "ValueError: wrong value")

    def test_keypress_q(self):
        try:
            raise ValueError("wrong value")
        except:
            widget = ErrorWidget(
                controller=self.controller,
                context=self.context
            )
        self.assertEqual(widget.keypress(None, "q"), None)
        self.controller.back.assert_called_with()
