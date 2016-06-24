"""Data Store

Contents:

* `StaticDataStore`: abstract class for data store
* `BaseStaticDataStore`: basic data store for static fixed list
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


class BaseStaticDataStore(BaseDataStore):
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
