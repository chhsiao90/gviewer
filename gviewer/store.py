"""Data Store

Contents:

* `StaticDataStore`: abstract class for data store
* `BaseStaticDataStore`: basic data store for static fixed list
"""


class BaseDataStore(object):
    def __init__(self):
        self.walker = None

    def register_walker(self, walker):
        """ register_walker
        """
        self.walker = walker

    def set_up(self):
        """ set_up
        """
        raise NotImplementedError


class BaseStaticDataStore(BaseDataStore):
    """ BaseStaticDataStore
    """
    def __init__(self, messages):
        self.messages = messages
        super(BaseDataStore, self).__init__()

    def set_up(self):
        """ create_walker
        """
        for message in self.messages:
            self.walker.recv(message)
