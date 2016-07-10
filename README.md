# General Viewer (GViewer)

#### Simple, Light Weight, but Powerful 
GViewer is a tui(Terminal UI) library that depends on [urwid](https://github.com/urwid/urwid) simplified writing a tui based reporting system.
You could just write less code, and the library could help you display the data.


## Installation
```
pip install gviewer
```


## Usage
#### Data Store
- BaseStaticDataStore
```python
data_store = BaseStaticDataStore(data)
```
- Custom Implementation
```python
class CustomDataStore(BasicDataStore):
    def set_up(self):
        # your implementation
```

#### Displayer
```python
class MyDisplayer(BaseDisplayer):
    def to_summary(self, message):
        # your implementation
        # return a str or text markup
        # reference: http://urwid.org/manual/displayattributes.html#text-markup

    def get_detail_displayers(self):
        # your implementation
        # return an array of tuple that contains detail view title and a function that transform message to detail
        # return [("title1", self.detail1), ("title2", self.detail2), ("title3", self.any_name_you_want)]

    def detail1(self, message):
        # return DetailGroup
```

#### GViewer
```python
viewer = GViewer(data_store, displayer)
viewer.start()
```

## Contribution
Please feel free to create issue or create PR
