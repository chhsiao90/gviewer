from .keys import vim
from .styles import default


class Config(object):
    """Config for GViewer

    Attributes:
        header: header content
        keys: dictionary define key mapping
        template: list of tuple for default stylesheet
    """
    def __init__(self,
                 header="General Viewer",
                 keys=vim,
                 template=default,
                 auto_scroll=False):
        self.header = header
        self.keys = keys
        self.template = template
        self.auto_scroll = auto_scroll
