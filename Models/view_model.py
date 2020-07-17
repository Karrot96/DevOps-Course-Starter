from flask import url_for


class ViewModel:
    def __init__(self, itmes):
        self._add_urls(itmes)

    @property
    def items(self):
        return self._uncompleted_items + self._completed_items

    @property
    def uncompleted_items(self):
        return self._uncompleted_items

    @property
    def completed_items(self):
        return self._completed_items

    def _add_urls(self, items):
        self._uncompleted_items = [
            item.add_url(
                url_for('complete_items', id=item.id)
            ) for item in items if not item.completed
        ]
        self._completed_items = [
            item.add_url(
                url_for('undo_complete', id=item.id)
            ) for item in items if item.completed
        ]