import glob
from pygments.lexers import get_lexer_by_name

from gviewer.util import pygmentize
from gviewer import StaticDataStore, GViewer, BaseDisplayer, DisplayerContext
from gviewer import Text, Group, View


def _get_list():
    return glob.glob("./**/*.py") + glob.glob("./**/*.json")


class Displayer(BaseDisplayer):
    def __init__(self):
        store = StaticDataStore(_get_list())
        context = DisplayerContext(store, self)
        self.viewer = GViewer(context)

    def get_views(self):
        return [("", self.highlight)]

    def highlight(self, message):
        with open(message, "r") as f:
            file_content = f.read()

        if message.endswith(".py"):
            pygmentize_list = pygmentize(file_content, get_lexer_by_name("python"))
        else:
            pygmentize_list = pygmentize(file_content, get_lexer_by_name("json"))

        widgets = map(lambda l: Text(l), pygmentize_list)

        return View([Group("", widgets)])

    def start(self):
        self.viewer.start()


def main():
    Displayer().start()

if __name__ == "__main__":
    main()
