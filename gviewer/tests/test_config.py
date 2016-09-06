import unittest

from gviewer.config import Config
from gviewer.keys import vim
from gviewer.styles import default


class TestConfig(unittest.TestCase):
    def test_default_value(self):
        config = Config()

        self.assertEqual(config.header, "General Viewer")
        self.assertEqual(config.keys, vim)
        self.assertEqual(config.template, default)
