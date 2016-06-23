import urwid


""" Summary Widget Related Component

Contents:

* `SummaryItem`: One line of the SummaryList
* `SummaryListWalker`: The urwid Walker to iterate over the data_store*
* `SummaryList`: urwid ListBox to display Summary

"""


class SummaryItem(urwid.WidgetWrap):
    def __init__(self, parent, displayer, message):
        self.parent = parent
        self.displayer = displayer
        self.message = message
        super(SummaryItem, self).__init__(self._make_widget())

    def _make_widget(self):
        title = self.displayer.to_summary(self.message)
        return urwid.AttrMap(
            urwid.Text(title), "summary", "summary focus")

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == "enter":
            self.parent.open_detail(self.message)
            return None
        return key


class SummaryListWalker(urwid.SimpleFocusListWalker):
    def __init__(self, parent, data_store, displayer):
        self.parent = parent
        self.data_store = data_store
        self.displayer = displayer
        super(SummaryListWalker, self).__init__([])

        data_store.register_walker(self)

    def recv(self, message):
        self.append(SummaryItem(self.parent, self.displayer, message))


class SummaryList(urwid.ListBox):
    def __init__(self, walker):
        super(SummaryList, self).__init__(walker)
