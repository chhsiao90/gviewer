# General Viewer (GViewer)
[![Build Status](https://travis-ci.org/chhsiao90/gviewer.svg?branch=master)](https://travis-ci.org/chhsiao90/gviewer)
[![Coverage Status](https://coveralls.io/repos/github/chhsiao90/gviewer/badge.svg)](https://coveralls.io/github/chhsiao90/gviewer)

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
from gviewer import BaseDisplayer, Groups, Group, PropsGroup, Line, Prop

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
        return Groups(
            [Group("title", [Line(m) for m in message["view1"]])]
        )

    def view2(self, message):
        """return groups"""
        return Groups(
            [PropsGroup("title", [Prop(p[0], p[1]) for p in message["view2"]])]
        )
```

#### GViewer
```python
from gviewer import GViewer
viewer = GViewer(data_store, displayer)
viewer.start()
```

## Contribution
Please feel free to create issue or create PR
