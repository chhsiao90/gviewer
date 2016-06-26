"""Data Store

Contents:

* `BaseDataStore`: abstract class for data store
* `StaticDataStore`: basic data store for static fixed list
* `AsyncDataStore`: async data store, like zmq, asyncio, etc...
"""


class BaseDataStore(object):
    """
    Base absctract class for data store

    Please extend it with set_up implementation
    """
    def __init__(self):
        self.walker = None

    def register_walker(self, walker):
        self.walker = walker

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
            self.walker.recv(message)


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
        self.register_func(self.walker.recv)
