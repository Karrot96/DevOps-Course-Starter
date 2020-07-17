class ViewModel:
    def __init__(self, itmes):
        self._items = itmes

    @property
    def items(self):
        return self._items
