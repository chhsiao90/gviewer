""" Displayer

Contents:

* `BaseDisplayer`: absctract class for displayer
"""


class BaseDisplayer(object):
    def to_summary(self, message):
        """ to_summary
        """
        raise NotImplementedError

    def to_detail_groups(self, message):
        """ to_detail_groups
        """
        raise NotImplementedError
