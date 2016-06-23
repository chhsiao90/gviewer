import json
from gviewer import BaseStaticDataStore, GViewer, BaseDisplayer


with open("examples/panama-taiwan.json", "r") as data_file:
    data = json.load(data_file)


class PanamaDisplayer(BaseDisplayer):
    def to_summary(self, message):
        return u"[{0}][{1}] {2}".format(
            message["node_id"],
            message["country_codes"],
            message["name"])

    def to_detail_groups(self, message):
        detail_groups = []
        summary_group_content = \
            [(k, v) for k, v in message.iteritems() if isinstance(v, str) or isinstance(v, unicode)]

        detail_groups.append(("Summary", summary_group_content))

        for shareholder in message.get("officers").get("shareholder of"):
            detail_groups.append((
                shareholder.get("name"),
                [(k, v) for k, v in shareholder.iteritems() if isinstance(v, str) or isinstance(v, unicode)]))

        return detail_groups


def main():
    data_store = BaseStaticDataStore(data)
    viewer = GViewer(data_store, PanamaDisplayer())
    viewer.start()

if __name__ == "__main__":
    main()
