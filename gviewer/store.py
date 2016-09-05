class BaseDataStore(object):
    """ Base absctract class for data store

    Attributes:
        walkers: list of Walkers, that would listener any message received from data store
    """
    def __init__(self):
        self.walkers = []

    def on_message(self, message):
        transformed_msg = self.transform(message)
        for walker in self.walkers:
            walker.recv(transformed_msg)

    def register(self, walker):
        self.walkers.append(walker)

    def unregister(self, walker):
        self.walkers.remove(walker)

    def transform(self, msg):
        return msg

    def setup(self):
        raise NotImplementedError


class StaticDataStore(BaseDataStore):
    """
    Used for static unmodified data that load data at first time

    Attributes:
        messages: list of any type of message
    """
    def __init__(self, messages):
        super(StaticDataStore, self).__init__()
        self.messages = messages

    def setup(self):
        for message in self.messages:
            self.on_message(message)


class AsyncDataStore(BaseDataStore):
    """
    Used for async data

    Attributes:
        register_func: callable that would accept a callable for on_message callback
    """
    def __init__(self, register_func):
        super(AsyncDataStore, self).__init__()
        self.register_func = register_func

    def setup(self):
        self.register_func(self.on_message)
