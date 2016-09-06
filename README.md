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
def register_func(on_message):
    some_listener.on_message(on_message)

data_store = AsyncDataStore(register_func)
```

#### Displayer
```python
from gviewer import BaseDisplayer, View, Group, PropsGroup, Text, Prop

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
            [Group("title", [Text(m) for m in message["view1"]])]
        )

    def view2(self, message):
        """return groups"""
        return View(
            [PropsGroup("title", [Prop(p[0], p[1]) for p in message["view2"]])]
        )
```

#### GViewer
```python
from gviewer import GViewer, DisplayerContext
context = DisplayerContext(data_store, displayer)
viewer = GViewer(context)
viewer.start()
```

## Advanced Usage
#### Summary Actions
Bind function to specific key to apply customize action, ex: export
```python
from gviewer import GViewer, DisplayerContext

def custom_export(controller, message, widget, *args, **kwargs):
    with open("export", "w") as f:
        f.write(str(message))
    controller.notify("file is export")

context = DisplayerContext(data_store, displayer, actions=Actions([("a", "Custom export", custom_export)]))
viewer = GViewer(context)
```

#### View Actions
Bind function to specific key to apply customize action, ex: export
```python
from gviewer import View, BaseDisplayer
class MyDisplayer(BaseDisplayer):
    def get_views(self):
        return [("view", self.view)]

    def view(self, message):
        return View([], actions=Actions([("a", "Custom export", self.custom_export)]))

    def custom_export(controller, message, *args, **kwargs):
        with open("export", "w") as f:
            f.write(str(message))
        controller.notify("file is export")
```

## Built-in actions
#### Summary
- /: search
- g: top
- G: bottom
- x: clear current item
- X: clear all items
- q: quit
- ?: help

#### Detail
- /: search
- tab: next view
- shift+tab: prev view
- n: search next result 
- N: search previous result
- e: export current content to file
- q: quit
- ?: help


## Contribution
Please feel free to create issue or create PR
