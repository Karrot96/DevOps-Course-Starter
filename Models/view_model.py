from flask import url_for
from datetime import datetime


def _today():
    return datetime.date(datetime.today())


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

    @property
    def recent_done_items(self):
        return [item for item in self._completed_items if datetime.date(item.last_updated) == _today()]

    @property
    def older_done_items(self):
        return [item for item in self._completed_items if datetime.date(item.last_updated) < _today()]

    @property
    def show_all_done_items(self):
        return len(self.completed_items) < 5

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