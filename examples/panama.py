import json
from gviewer import StaticDataStore, GViewer, BaseDisplayer, DisplayerContext
from gviewer import Prop, PropsGroup, View, Actions


with open("examples/panama-taiwan.json", "r") as data_file:
    data = json.load(data_file)


class PanamaDisplayer(BaseDisplayer):
    def __init__(self, data):
        data_store = self.create_data_store(data)
        self.child_context = ChildDisplayer().context
        self.viewer = GViewer(
            DisplayerContext(data_store, self, actions=Actions(
                [("m", "notify a message", self.notify),
                 ("L", "log view", self.log)])),
            other_contexts=[self.child_context],
            palette=[("nodeid", "light cyan", "black")])

    def create_data_store(self, data):
        return StaticDataStore(data)

    def summary(self, message):
        return [
            ("nodeid", message["node_id"]),
            " ",
            message["name"]]

    def get_views(self):
        return [("Detail", self.detail)]

    def detail(self, message):
        detail_groups = []
        summary_group_content = \
            [Prop(k, v) for k, v in message.iteritems() if isinstance(v, str) or isinstance(v, unicode)]

        detail_groups.append(PropsGroup("Summary", summary_group_content))

        for shareholder in message.get("officers").get("shareholder of"):
            detail_groups.append(PropsGroup(
                shareholder.get("name"),
                [Prop(k, v) for k, v in shareholder.iteritems() if isinstance(v, str) or isinstance(v, unicode)]))

        return View(detail_groups, actions=Actions([
            ("E", "export", self.export),
            ("m", "notify", self.notify)]))

    def notify(self, controller, messag):
        controller.notify("yayaya")

    def export(self, controller, message):
        with open("panama-export.json", "w") as w:
            w.write(json.dumps(message))
        controller.notify("export to file panama-export.json")

    def log(self, controller, message):
        controller.open_view_by_context(self.child_context)

    def run(self):
        self.viewer.start()


class ChildDisplayer(BaseDisplayer):
    def __init__(self):
        store = StaticDataStore(["log1: aaabbbccc",
                                 "log2: hahahaha",
                                 "log3: yayayayaya"])
        self.context = DisplayerContext(store, self)


def main():
    PanamaDisplayer(data).run()

if __name__ == "__main__":
    main()
