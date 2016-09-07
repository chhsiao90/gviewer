import glob
from pygments import lexers

from gviewer.util import pygmentize
from gviewer import StaticDataStore, GViewer, BaseDisplayer, DisplayerContext
from gviewer import Text, Group, View


def _get_py_list():
    return glob.glob("./**/*.py")


class Displayer(BaseDisplayer):
    def __init__(self):
        store = StaticDataStore(_get_py_list())
        context = DisplayerContext(store, self)
        self.viewer = GViewer(context)

    def get_views(self):
        return [("", self.highlight)]

    def highlight(self, message):
        with open(message, "r") as f:
            file_content = f.read()

        pygmentize_list = pygmentize(file_content, lexers.PythonLexer())
        widgets = map(lambda l: Text(l), pygmentize_list)

        return View([Group("", widgets)])

    def start(self):
        self.viewer.start()


def main():
    Displayer().start()

if __name__ == "__main__":
    main()
