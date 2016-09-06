import unittest
import mock

from gviewer.action import Action, Actions


class ActionTest(unittest.TestCase):
    def test_call(self):
        function = mock.Mock()
        action = Action("desc", function)

        action.__call__()
        function.assert_called_with()

        action.__call__("aaa")
        function.assert_called_with("aaa")

        action.__call__(aaa="bbb")
        function.assert_called_with(aaa="bbb")


class ActionsTest(unittest.TestCase):
    def setUp(self):
        self.func_a = mock.Mock()
        self.func_b = mock.Mock()
        self.actions = Actions([
            ("a", "haha", self.func_a),
            ("b", "yaya", self.func_b)])

    def test_iter(self):
        action_list = [a for a in self.actions]
        self.assertEqual(len(action_list), 2)
        self.assertEqual(
            action_list[0],
            ("a", "haha", self.func_a))
        self.assertEqual(
            action_list[1],
            ("b", "yaya", self.func_b))

    def test_contains(self):
        self.assertTrue("a" in self.actions)
        self.assertTrue("b" in self.actions)
        self.assertFalse("c" in self.actions)

    def test_getitem(self):
        action = self.actions["a"]
        self.assertIsInstance(action, Action)
        self.assertEqual(action.desc, "haha")
