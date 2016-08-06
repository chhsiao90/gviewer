import unittest

from gviewer.element import Line, SearchableWidget, Prop, Group, PropsGroup
from gviewer.view import TitleWidget, ItemWidget


class LineTest(unittest.TestCase):
    def test_line_widget(self):
        widget = Line("content").to_widget()
        self.assertTrue(isinstance(widget, SearchableWidget))


class PropTest(unittest.TestCase):
    def test_prop_widget(self):
        widget = Prop("key", "value").to_widget()
        text, attr = widget.get_text()
        self.assertEqual(
            text,
            "key: value"
        )
        self.assertEqual(
            attr,
            [("view-item key", 5),
             ("view-item value", 5)]
        )

    def test_prop_widget_with_padding(self):
        prop = Prop("key", "value")
        prop.max_key_length = 5
        self.assertEqual(
            prop.to_widget().get_text()[0],
            "key   : value"
        )


class GroupTest(unittest.TestCase):
    def test_group_widget_with_title(self):
        widgets = Group(
            "title",
            items=[
                Line("first line"),
                Line("second line")]
        ).to_widgets()

        self.assertEqual(len(widgets), 3)
        self.assertTrue(isinstance(widgets[0], TitleWidget))
        self.assertTrue(isinstance(widgets[1], ItemWidget))
        self.assertTrue(isinstance(widgets[2], ItemWidget))

    def test_group_widget_without_title(self):
        widgets = Group(
            "title",
            items=[
                Line("first line"),
                Line("second line")],
            show_title=False).to_widgets()

        self.assertEqual(len(widgets), 2)
        self.assertTrue(isinstance(widgets[0], ItemWidget))
        self.assertTrue(isinstance(widgets[1], ItemWidget))


class PropsGroupTest(unittest.TestCase):
    def test_calc_key_length(self):
        props_group = PropsGroup(
            "title",
            items=[
                Prop("key", "value"),
                Prop("longkey", "value"),
                Prop("k", "value")]
        )
        self.assertEqual(props_group.items[0].max_key_length, 7)
        self.assertEqual(props_group.items[1].max_key_length, 7)
        self.assertEqual(props_group.items[2].max_key_length, 7)


if __name__ == "__main__":
    unittest.main()
