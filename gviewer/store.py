class BaseDataStore(object):
    """ Base absctract class for data store

    Attributes:
        walkers
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

    :param message: the data you want to display
    :type message: iterable for any type data
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

    :param register_func: register function that would be called while setup
    :type register_func: function accept one parameter with function(message)
    """
    def __init__(self, register_func):
        super(AsyncDataStore, self).__init__()
        self.register_func = register_func

    def setup(self):
        self.register_func(self.on_message)
