from Models.view_model import ViewModel
from Models import view_model
from Models.item import Item
from dateutil import parser
import pytest

DATE_FOR_USE = "2020-01-01T12:00:00"


@pytest.fixture
def today():
    return "2020-01-03T12:00:00"

@pytest.fixture
def yesterday():
    return "2020-01-02T12:00:00"


@pytest.fixture(autouse=True)
def mock_response_url_for(monkeypatch):
    def mock_url_for(*args, **kwargs):
        return kwargs
    monkeypatch.setattr(view_model, "url_for", mock_url_for)

@pytest.fixture(autouse=True)
def mock_response_today(monkeypatch, today):
    def mock_today(*args, **kwargs):
        return parser.isoparse(today).replace(tzinfo=None)
    monkeypatch.setattr(view_model, "_today", mock_today)


@pytest.fixture
def uncompleted_item():
    return Item(1, False, "Item1", DATE_FOR_USE)

@pytest.fixture
def completed_item():
    return Item(2, True, "Item2",  DATE_FOR_USE)


def test_view_model_returns_all_items(completed_item, uncompleted_item):
    items = [
        uncompleted_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item in view_model_output.items
    assert completed_item in view_model_output.items


def test_view_model_returns_only_completed_items(completed_item, uncompleted_item):
    items = [
        uncompleted_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item not in view_model_output.completed_items
    assert completed_item in view_model_output.completed_items


def test_view_model_returns_only_uncompleted_items(completed_item, uncompleted_item):
    items = [
        uncompleted_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item in view_model_output.uncompleted_items
    assert completed_item not in view_model_output.uncompleted_items


def test_view_model_return_all_completed_items():
    items = [Item(item_id, True, "Test",  DATE_FOR_USE) for item_id in range(0, 4)]
    view_model_output = ViewModel(items)

    assert view_model_output.show_all_done_items


def test_view_model_does_not_return_all_completed_tiems():
    items = [Item(item_id, True, "Test",  DATE_FOR_USE) for item_id in range(0, 6)]
    view_model_output = ViewModel(items)

    assert not view_model_output.show_all_done_items


def test_recent_done_items_returns_items_completed_today(today, yesterday):
    item_today = Item(1, True, "Test", today)
    item_yesterday = Item(2, True, "Test", yesterday)

    view_model = ViewModel([item_today, item_yesterday])

    assert item_today in view_model.recent_done_items
    assert item_yesterday not in view_model.recent_done_items

def test_older_done_items_returns_items_not_completed_today(today, yesterday):
    item_today = Item(1, True, "Test", today)
    item_yesterday = Item(2, True, "Test", yesterday)

    view_model = ViewModel([item_today, item_yesterday])

    assert item_today not in view_model.older_done_items
    assert item_yesterday in view_model.older_done_items