class BaseDataStore(object):
    """ Base absctract class for data store

    Attributes:
        msg_listener: MessageListener instance
    """
    def __init__(self):
        self.msg_listener = None  # pragma: no cover

    def register_listener(self, msg_listener):
        """ Register msg_listener

        Register msg_listener, will be called before GViewer start
        """
        self.msg_listener = msg_listener

    def transform(self, msg):
        return msg

    def set_up(self):
        raise NotImplementedError


class StaticDataStore(BaseDataStore):
    """
    Used for static unmodified data that load data at first time

    :param message: the data you want to display
    :type message: iterable for any type data
    """
    def __init__(self, messages):
        self.messages = messages
        super(BaseDataStore, self).__init__()

    def set_up(self):
        for message in self.messages:
            self.msg_listener.on_message(message)


class AsyncDataStore(BaseDataStore):
    """
    Used for async data

    :param register_func: register function that would be called while set_up
    :type register_func: function accept one parameter with function(message)
    """
    def __init__(self, register_func):
        self.register_func = register_func
        super(BaseDataStore, self).__init__()

    def set_up(self):
        self.register_func(self.msg_listener.on_message)


class MessageListener(object):
    def __init__(self, data_store):
        self.data_store = data_store
        self.walkers = []
        self.data_store.register_listener(self)

    def on_message(self, message):
        transformed_msg = self.data_store.transform(message)
        for walker in self.walkers:
            walker.recv(transformed_msg)

    def register(self, walker):
        self.walkers.append(walker)

    def unregister(self, walker):
        self.walkers.remove(walker)
