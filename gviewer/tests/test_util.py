import unittest
from pygments import lexers, token

from gviewer.util import pygmentize, _join


class TestUtil(unittest.TestCase):
    def test_pygmentize(self):
        python_content = """
        import unittest

        class Pygmentize(object):
            pass"""
        result = pygmentize(python_content, lexers.PythonLexer())

        self.assertEqual(len(result), 4)

        self.assertIn(
            (token.Token.Keyword.Namespace, u'import'),
            result[0])
        self.assertIn(
            (token.Token.Name.Namespace, u'unittest'),
            result[0])

        self.assertEqual(result[1], u"")

        self.assertIn(
            (token.Token.Keyword, u'class'),
            result[2])
        self.assertIn(
            (token.Token.Name.Class, u'Pygmentize'),
            result[2])

        self.assertIn(
            (token.Token.Keyword, u'pass'),
            result[3])

    def test_join(self):
        result = _join([("aaa", "bbb"), ("ccc", "ddd")], "\n")
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0], [("aaa", "bbb"), ("ccc", "ddd")])
