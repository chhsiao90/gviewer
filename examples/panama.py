import json
from gviewer import StaticDataStore, GViewer, BaseDisplayer
from gviewer import DetailProp, DetailGroup


with open("examples/panama-taiwan.json", "r") as data_file:
    data = json.load(data_file)


class PanamaDisplayer(BaseDisplayer):
    def __init__(self, data):
        data_store = self.create_data_store(data)
        self.viewer = GViewer(
            data_store, self,
            palette=[("nodeid", "light cyan", "black")])

    def create_data_store(self, data):
        return StaticDataStore(data)

    def to_summary(self, message):
        return [
            ("nodeid", message["node_id"]),
            " ",
            message["name"]]

    def get_detail_displayers(self):
        return [("Detail", self.detail)]

    def detail(self, message):
        detail_groups = []
        summary_group_content = \
            [DetailProp(k, v) for k, v in message.iteritems() if isinstance(v, str) or isinstance(v, unicode)]

        detail_groups.append(DetailGroup("Summary", summary_group_content))

        for shareholder in message.get("officers").get("shareholder of"):
            detail_groups.append(DetailGroup(
                shareholder.get("name"),
                [DetailProp(k, v) for k, v in shareholder.iteritems() if isinstance(v, str) or isinstance(v, unicode)]))

        return detail_groups

    def run(self):
        self.viewer.start()


def main():
    PanamaDisplayer(data).run()

if __name__ == "__main__":
    main()
