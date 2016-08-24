import unittest
import sys

try:
    import unittest.mock as mock
except:
    import mock

from util import render_to_content
from gviewer.error import ErrorWidget


class ErrorWidgetTest(unittest.TestCase):
    def setUp(self):
        self.parent = mock.Mock()

    def test_render(self):
        try:
            raise ValueError("wrong value")
        except:
            widget = ErrorWidget(
                self.parent,
                sys.exc_info()
            )

        contents = render_to_content(widget, (100, 4))
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
                self.parent,
                sys.exc_info()
            )
        self.assertEqual(widget.keypress(None, "q"), None)
        self.parent.back.assert_called_with()


if __name__ == "__main__":
    unittest.main()
