from gviewer import StaticDataStore, GViewer, BaseDisplayer
from gviewer import Line, Group, Groups


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

    def summary(self, message):
        return message["summary"]

    def get_views(self):
        return [("View A", self.detail_a),
                ("View B", self.detail_b),
                ("View C", self.detail_c)]

    def detail_a(self, message):
        return Groups([Group("AAA", [Line(message["a"])])])

    def detail_b(self, message):
        return Groups([Group("BBB", [Line(message["b"])])])

    def detail_c(self, message):
        return Groups([Group("CCC", [Line(message["c"])])])

    def run(self):
        self.viewer.start()


def main():
    Displayer(data).run()

if __name__ == "__main__":
    main()
