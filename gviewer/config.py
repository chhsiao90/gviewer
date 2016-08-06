from keys import vim
from styles import default


""" General Viewer Config """


class Config(object):
    """
    config for GViewer
    :header param: header content
    :header type: str

    :keys param: key mapping, default is vim mode
    :keys type: dict
    """
    def __init__(self,
                 header="General Viewer",
                 keys=vim,
                 template=default):
        self.header = header
        self.keys = keys
        self.template = template
