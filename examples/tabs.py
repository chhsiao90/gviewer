from gviewer import StaticDataStore, GViewer, BaseDisplayer
from gviewer import DetailLine, DetailGroup


data = [{"summary": "summary a",
         "a": "detail a",
         "b": "detail b",
         "c": "detail c"},
        {"summary": "summary b",
         "a": "detail d",
         "b": "detail f",
         "c": "detail g"}]


class Displayer(BaseDisplayer):
    def __init__(self, data):
        data_store = StaticDataStore(data)
        self.viewer = GViewer(data_store, self)

    def to_summary(self, message):
        return message["summary"]

    def get_detail_displayers(self):
        return [("Detail A", self.detail_a),
                ("Detail B", self.detail_b),
                ("Detail C", self.detail_c)]

    def detail_a(self, message):
        return [DetailGroup("Detail", [DetailLine(message["a"])])]

    def detail_b(self, message):
        return [DetailGroup("Detail", [DetailLine(message["b"])])]

    def detail_c(self, message):
        return [DetailGroup("Detail", [DetailLine(message["c"])])]

    def run(self):
        self.viewer.start()


def main():
    Displayer(data).run()

if __name__ == "__main__":
    main()
