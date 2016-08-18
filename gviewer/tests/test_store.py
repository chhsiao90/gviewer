import unittest

try:
    import unittest.mock as mock
except:
    import mock

from gviewer.store import StaticDataStore, AsyncDataStore, MessageListener


class StaticDataStoreTest(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.listener.on_message = mock.Mock()

        self.data_store = StaticDataStore([
            "message 1", "message 2"])
        self.data_store.register_listener(self.listener)

    def test_set_up(self):
        self.data_store.set_up()
        self.listener.on_message.assert_has_calls(
            [mock.call("message 1"), mock.call("message 2")], any_order=True)


class AsyncDataStoreTest(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.listener.on_message = mock.Mock()

        self.register_func = mock.Mock()

        self.data_store = AsyncDataStore(self.register_func)
        self.data_store.register_listener(self.listener)

    def test_set_up(self):
        self.data_store.set_up()
        self.register_func.assert_called_with(
            self.listener.on_message)


class MessageListenerTest(unittest.TestCase):
    def setUp(self):
        self.data_store = mock.Mock()
        self.data_store.register_listener = mock.Mock()
        self.data_store.transform = mock.Mock(
            side_effect=lambda m: m)

        self.walker = mock.Mock()
        self.walker.recv = mock.Mock()

        self.listener = MessageListener(self.data_store)
        self.listener.register(self.walker)

    def test_init_with_register_listener(self):
        self.data_store.register_listener.assert_called_with(
            self.listener)

    def test_on_message(self):
        self.listener.on_message("message")
        self.walker.recv.assert_called_with(
            "message")

    def test_register(self):
        self.listener.register("another walker")
        self.assertEqual(
            self.listener.walkers,
            [self.walker, "another walker"]
        )

    def test_unregister(self):
        self.listener.unregister(self.walker)
        self.assertEquals(len(self.listener.walkers), 0)


if __name__ == "__main__":
    unittest.main()
