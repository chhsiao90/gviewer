from gviewer import StaticDataStore, GViewer, BaseDisplayer, DisplayerContext
from gviewer import Text, Group, View


data = [{"summary": "summary a",
         "a": ["detail a",
               "detail aa",
               "detail aaa",
               "detail aaaa"],
         "b": ["detail b"],
         "c": ["detail c"]},
        {"summary": "summary b",
         "a": ["detail d"],
         "b": ["detail f"],
         "c": ["detail g"]}]


class Displayer(BaseDisplayer):
    def __init__(self, data):
        data_store = StaticDataStore(data)
        self.viewer = GViewer(DisplayerContext(data_store, self))

    def summary(self, message):
        return message["summary"]

    def get_views(self):
        return [("View A", self.detail_a),
                ("View B", self.detail_b),
                ("View C", self.detail_c)]

    def detail_a(self, message):
        return View([Group("AAA", [Text(m) for m in message["a"]])])

    def detail_b(self, message):
        return View([Group("BBB", [Text(m) for m in message["b"]])])

    def detail_c(self, message):
        return View([Group("CCC", [Text(m) for m in message["c"]])])

    def run(self):
        self.viewer.start()


def main():
    Displayer(data).run()

if __name__ == "__main__":
    main()
