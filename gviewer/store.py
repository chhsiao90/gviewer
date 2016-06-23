

"""Data Store

Contents:

* `BaseStaticDataStore`: abstract class
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

    def to_summary(self, message):
        """ to_summary
        """
        raise NotImplementedError

    def to_detail_groups(self, message):
        """ to_detail_groups
        """
        raise NotImplementedError


class BaseStaticDataStore(BaseDataStore):
    """ BaseStaticDataStore
    """
    def __init__(self, messages):
        """
        """
        self.messages = messages
        super(BaseDataStore, self).__init__()

    def set_up(self):
        """ create_walker
        """
        for message in self.messages:
            self.walker.recv(message)
