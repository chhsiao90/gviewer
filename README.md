# General Viewer (GViewer)

GViewer is a tui(Terminal UI) library that simplified writing a tui based reporting system.


## Installation
```
pip install git+https://github.com/chhsiao90/gviewer.git
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

    def to_detail_groups(self, message):
        # your implementation
```

#### GViewer
```python
viewer = GViewer(data_store, displayer)
viewer.start()
```
