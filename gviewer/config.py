from keys import vim


""" General Viewer Config """


class Config(object):
    """
    config for GViewer
    :header param: header content
    :header type: str

    :keys param: key mapping, default is vim mode
    :keys type: dict
    """
    def __init__(self, header="General Viewer", keys=vim):
        self.header = header
        self.keys = keys
