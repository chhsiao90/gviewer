import urwid


class SummaryItem(urwid.WidgetWrap):
    def __init__(self, parent, data_store, message):
        self.parent = parent
        self.data_store = data_store
        self.message = message
        super(SummaryItem, self).__init__(self._make_widget())

    def _make_widget(self):
        title = self.data_store.to_summary(self.message)
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
    def __init__(self, parent, data_store):
        self.parent = parent
        self.data_store = data_store
        super(SummaryListWalker, self).__init__([])
        self.data_store.register_walker(self)

    def recv(self, message):
        self.append(SummaryItem(self.parent, self.data_store, message))


class SummaryList(urwid.ListBox):
    def __init__(self, parent, data_store, walker):
        self.parent = parent
        self.data_store = data_store
        super(SummaryList, self).__init__(walker)
