from gviewer import StaticDataStore, GViewer, BaseDisplayer, DetailDisplayer
from gviewer import DetailLine, DetailGroup


data = [{"summary": "summary a",
         "a": "detail a",
         "b": "detail b"},
        {"summary": "summary a",
         "a": "detail a",
         "b": "detail b"}]


class Displayer(BaseDisplayer):
    def __init__(self, data):
        data_store = StaticDataStore(data)
        self.viewer = GViewer(data_store, self)

    def to_summary(self, message):
        return message["summary"]

    def get_detail_displayers(self):
        return [("Detail A", SimpleDetailDisplayer("a")),
                ("Detail B", SimpleDetailDisplayer("b"))]

    def run(self):
        self.viewer.start()


class SimpleDetailDisplayer(DetailDisplayer):
    def __init__(self, char):
        self.char = char

    def to_detail_groups(self, message):
        return [DetailGroup("Detail", [DetailLine(message[self.char])])]


def main():
    Displayer(data).run()

if __name__ == "__main__":
    main()
