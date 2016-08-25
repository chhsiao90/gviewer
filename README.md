# General Viewer (GViewer)
[![Build Status](https://travis-ci.org/chhsiao90/gviewer.svg?branch=master)](https://travis-ci.org/chhsiao90/gviewer)
[![Coverage Status](https://coveralls.io/repos/github/chhsiao90/gviewer/badge.svg?branch=master)](https://coveralls.io/github/chhsiao90/gviewer?branch=master)

##### Simple, Light Weight, but Powerful 
GViewer is a terminal UI library that depends on [urwid](https://github.com/urwid/urwid) simplified writing a tui based reporting system.
You could just write less code, and the library could help you display the data.

## Installation
```
pip install gviewer
```

## Usage
#### Data Store
- StaticDataStore
```python
from gviewer import StaticDataStore
data_store = StaticDataStore(data)
```

- AsyncDataStore
```python
data_store = AsyncDataStore(register_func)
```

#### Displayer
```python
from gviewer import BaseDisplayer, View, Group, PropsGroup, Line, Prop

class MyDisplayer(BaseDisplayer):
    def to_summary(self, message):
        """
        return a str or text markup
        reference: http://urwid.org/manual/displayattributes.html#text-markup
        """
        return message["summary"]

    def get_views(self):
        """return an array of tuple that contains view title and a function that transform message to detail"""
        return [
            ("view1", self.view1),
            ("view2", self.view2),
        ]

    def view1(self, message):
        """return groups"""
        return View(
            [Group("title", [Line(m) for m in message["view1"]])]
        )

    def view2(self, message):
        """return groups"""
        return View(
            [PropsGroup("title", [Prop(p[0], p[1]) for p in message["view2"]])]
        )
```

#### GViewer
```python
from gviewer import GViewer
viewer = GViewer(data_store, displayer)
viewer.start()
```

## Advanced Usage
#### Summary Actions
Bind function to specific key to apply customize action, ex: export
```python
from gviewer import GViewer

def custom_export(parent, message):
    with open("export", "w") as f:
        f.write(str(message))
    parent.notify("file is export")
viewer = GViewer(data_store, displayer, summary_actions=dict(a=custom_export))
```

#### View Actions
Bind function to specific key to apply customize action, ex: export
```python
from gviewer import View, BaseDisplayer, Groups
class MyDisplayer(BaseDisplayer):
    def get_views(self):
        return [("view", self.view)]

    def view(self, message):
        return View(Groups([]), actions=dict(a=self.custom_export))

    def custom_export(parent, message):
        with open("export", "w") as f:
            f.write(str(message))
        parent.notify("file is export")
```

## Contribution
Please feel free to create issue or create PR
