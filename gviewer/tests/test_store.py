import unittest
import mock

from gviewer.store import StaticDataStore, AsyncDataStore


class StaticDataStoreTest(unittest.TestCase):
    def setUp(self):
        self.walker = mock.Mock()

        self.data_store = StaticDataStore([
            "message 1", "message 2"])
        self.data_store.register(self.walker)

    def test_setup(self):
        self.assertEqual(len(self.data_store.walkers), 1)

        self.data_store.setup()
        self.walker.recv.assert_has_calls(
            [mock.call("message 1"), mock.call("message 2")], any_order=True)

    def test_register_new_walker(self):
        walker2 = mock.Mock()
        self.data_store.register(walker2)

        self.assertEqual(len(self.data_store.walkers), 2)

        self.data_store.setup()
        self.walker.recv.assert_has_calls(
            [mock.call("message 1"), mock.call("message 2")], any_order=True)
        walker2.recv.assert_has_calls(
            [mock.call("message 1"), mock.call("message 2")], any_order=True)

    def test_unregister(self):
        self.data_store.unregister(self.walker)
        self.assertEqual(len(self.data_store.walkers), 0)


class AsyncDataStoreTest(unittest.TestCase):
    def setUp(self):
        self.walker = mock.Mock()

        self.register_func = mock.Mock()

        self.data_store = AsyncDataStore(self.register_func)
        self.data_store.register(self.walker)

    def test_setup(self):
        self.data_store.setup()
        self.register_func.assert_called_with(
            self.data_store.on_message)
