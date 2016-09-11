import unittest
import mock
import urwid

from gviewer.basic_widget import BasicWidget, FocusableText, SearchWidget, SearchableText


class TestBasicWidget(unittest.TestCase):
    def setUp(self):
        self.context = mock.Mock()
        self.controller = mock.Mock()
        self.context.config.keys = dict()

    def test_display(self):
        widget = BasicWidget()

        text = urwid.Text("This is text")
        widget.display(text)
        self.assertEqual(widget._w, text)

        text = urwid.Text("Another text")
        self.assertNotEqual(widget._w, text)
        widget.display(text)
        self.assertEqual(widget._w, text)

    def test_keypress(self):
        self.context.config.keys.update(dict(
            h="left",
            j="down",
            k="up",
            l="right"
        ))

        widget = mock.Mock()
        widget.keypress = lambda size, key: key
        widget = BasicWidget(
            controller=self.controller,
            context=self.context,
            widget=widget)

        self.assertEqual(widget.keypress((1,), "h"), "left")
        self.assertEqual(widget.keypress((1,), "left"), "left")

        self.assertEqual(widget.keypress((1,), "j"), "down")
        self.assertEqual(widget.keypress((1,), "down"), "down")

        self.assertEqual(widget.keypress((1,), "k"), "up")
        self.assertEqual(widget.keypress((1,), "up"), "up")

        self.assertEqual(widget.keypress((1,), "l"), "right")
        self.assertEqual(widget.keypress((1,), "right"), "right")

    def test_keypress_when_editing(self):
        self.context.config.keys.update(dict(
            h="left",
            j="down",
            k="up",
            l="right"
        ))

        widget = mock.Mock()
        widget.keypress = lambda size, key: key
        widget = BasicWidget(
            context=self.context,
            widget=widget)
        widget.is_editing = lambda: True

        self.assertEqual(widget.keypress((1,), "h"), "h")
        self.assertEqual(widget.keypress((1,), "j"), "j")
        self.assertEqual(widget.keypress((1,), "k"), "k")
        self.assertEqual(widget.keypress((1,), "l"), "l")


class TestFocusableText(unittest.TestCase):
    def test_contains_markup(self):
        text = FocusableText([("attr1", "text1"), ("attr2", "text2"), "text3"])

        self.assertEqual(
            [w for w in text.render((15,), False).content()],
            [[("attr1", None, b"text1"),
              ("attr2", None, b"text2"),
              (None, None, b"text3")]]
        )

        self.assertEqual(
            [w for w in text.render((15,), True).content()],
            [[(None, None, b"text1text2text3")]]
        )

    def test_plain_text(self):
        text = FocusableText("plaintext")

        self.assertEqual(
            [w for w in text.render((9,), False).content()],
            [[(None, None, b"plaintext")]]
        )

        self.assertEqual(
            [w for w in text.render((9,), True).content()],
            [[(None, None, b"plaintext")]]
        )


class TestSearchWidget(unittest.TestCase):
    def setUp(self):
        self.search_func = mock.Mock()
        self.clear_func = mock.Mock()
        self.widget = SearchWidget(
            self.search_func,
            self.clear_func
        )

    def test_invoke_search(self):
        self.widget.keypress((10,), "a")
        self.widget.keypress((10,), "b")
        self.widget.keypress((10,), "c")
        self.widget.keypress((10,), "enter")

        self.assertEqual(
            self.widget.get_keyword(),
            "abc")
        self.search_func.assert_called_with("abc")

    def test_invoke_clear(self):
        self.widget.keypress((10,), "a")
        self.widget.keypress((10,), "b")
        self.widget.keypress((10,), "c")
        self.widget.keypress((10,), "esc")

        self.assertEqual(
            self.widget.get_keyword(),
            "")
        self.clear_func.assert_called_with()


class TestSearchableText(unittest.TestCase):
    def test_found_next_one(self):
        widget = SearchableText("aaamatchbbb")
        self.assertTrue(widget.search_next("match"))
        self.assertEqual(widget.prev_index, (8, 3))
        self.assertFalse(widget.search_next("match"))

    def test_found_prev_one(self):
        widget = SearchableText("aaamatchbbb")
        self.assertTrue(widget.search_prev("match"))
        self.assertEqual(widget.prev_index, (8, 3))
        self.assertFalse(widget.search_prev("match"))

    def test_search_with_two_match(self):
        widget = SearchableText("aaamatchbbbmatchccc")
        self.assertTrue(widget.search_next("match"))
        self.assertEqual(widget.prev_index, (8, 3))
        self.assertTrue(widget.search_next("match"))
        self.assertEqual(widget.prev_index, (16, 11))
        self.assertTrue(widget.search_prev("match"))
        self.assertEqual(widget.prev_index, (8, 3))

    def test_search_in_markup(self):
        widget = SearchableText([("no-match", "aaa"), " xxx ", ("yaya", "match"), " match ", ("end", "end")])

        self.assertTrue(widget.search_next("match"))
        self.assertEqual(widget.prev_index, (3, 2))
        self.assertEqual(
            widget._w.get_text(),
            (u"aaa xxx match match end", [("no-match", 3), (None, 5), ("match", 5), (None, 7), ("end", 3)]))

        self.assertTrue(widget.search_next("match"))
        self.assertEqual(widget.prev_index, (4, 3))
        self.assertEqual(
            widget._w.get_text(),
            (u"aaa xxx match match end", [("no-match", 3), (None, 5), ("yaya", 5), (None, 1), ("match", 5), (None, 1), ("end", 3)]))

        self.assertFalse(widget.search_next("match"))
        self.assertEqual(
            widget._w.get_text(),
            urwid.Text(widget.text).get_text())

        self.assertTrue(widget.search_prev("match"))
        self.assertEqual(widget.prev_index, (4, 3))
        self.assertEqual(
            widget._w.get_text(),
            (u"aaa xxx match match end", [("no-match", 3), (None, 5), ("yaya", 5), (None, 1), ("match", 5), (None, 1), ("end", 3)]))

        self.assertTrue(widget.search_prev("match"))
        self.assertEqual(widget.prev_index, (3, 2))
        self.assertEqual(
            widget._w.get_text(),
            (u"aaa xxx match match end", [("no-match", 3), (None, 5), ("match", 5), (None, 7), ("end", 3)]))

        self.assertFalse(widget.search_prev("match"))
        self.assertEqual(
            widget._w.get_text(),
            urwid.Text(widget.text).get_text())
