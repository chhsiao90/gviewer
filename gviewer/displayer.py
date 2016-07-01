""" Displayer """


class BaseDisplayer(object):
    """ absctract class for displayer """
    def to_summary(self, message):
        """
        define how message display in summary widget
        :param message: message that defined at DataStore implementation
        :type message: depend on DataStore

        Return str
        """
        raise NotImplementedError

    def match(self, search, message, summary):
        """
        define is that the message match the search pattern

        :param search: search keyword
        :type search: str

        :param message: message that defined at DataStore implementation
        :type message: depend on DataStore

        Return Ture or False
        """
        return search in summary

    def get_detail_displayers(self):
        """
        return a list of tuple that contains view name and a DetailDisplayer
        """
        raise NotImplementedError


class DetailDisplayer(object):
    def to_detail_groups(self, message):
        """
        define how message display in detail
        :param message: message that defined at DataStore implementation
        :type message: depend on DataStore

        Return a list of tuple (groupName, gruopContent)
        groupContent is a list of tuple (key, value)
        example: [("block1", [("prop1", "value1"), ("prop2", "value2)],
                  ("block2", [("prop3", "value3")])]
        """
        raise NotImplementedError
