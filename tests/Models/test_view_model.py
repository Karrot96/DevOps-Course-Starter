from todo_app.models.view_model import ViewModel
from todo_app.models import view_model
from todo_app.models.item import Item, Status
import pytest
from datetime import datetime

DATE_FOR_USE = datetime(2020, 1, 1, 12, 00, 00)


@pytest.fixture
def today():
    return datetime(2020, 1, 3, 12, 00,00)

@pytest.fixture
def yesterday():
    return datetime(2020, 1, 2, 12, 00, 00)


@pytest.fixture(autouse=True)
def mock_response_url_for(monkeypatch):
    def mock_url_for(*args, **kwargs):
        return kwargs
    monkeypatch.setattr(view_model, "url_for", mock_url_for)

@pytest.fixture(autouse=True)
def mock_response_today(monkeypatch, today):
    def mock_today(*args, **kwargs):
        return datetime.date(today)
    monkeypatch.setattr(view_model, "_today", mock_today)


@pytest.fixture
def uncompleted_item():
    return Item(1, Status.TODO, "Item1", DATE_FOR_USE)

@pytest.fixture
def completed_item():
    return Item(2, Status.DONE, "Item2",  DATE_FOR_USE)

@pytest.fixture
def doing_item():
    return Item(3, Status.DOING, "Item3", DATE_FOR_USE)


def test_view_model_returns_all_items(completed_item, uncompleted_item, doing_item):
    items = [
        uncompleted_item,
        doing_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert items == view_model_output.items


def test_view_model_returns_only_completed_items(completed_item, uncompleted_item, doing_item):
    items = [
        uncompleted_item,
        completed_item,
        doing_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item not in view_model_output.completed_items
    assert completed_item in view_model_output.completed_items
    assert doing_item not in view_model_output.completed_items


def test_view_model_returns_only_uncompleted_items(completed_item, uncompleted_item, doing_item):
    items = [
        uncompleted_item,
        completed_item, doing_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item in view_model_output.uncompleted_items
    assert completed_item not in view_model_output.uncompleted_items
    assert doing_item not in view_model_output.uncompleted_items


def test_view_model_returns_only_doing_items(completed_item, uncompleted_item, doing_item):
    items = [
        uncompleted_item,
        completed_item,
        doing_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item not in view_model_output.doing_items
    assert completed_item not in view_model_output.doing_items
    assert doing_item in view_model_output.doing_items


def test_view_model_return_all_completed_items():
    items = [Item(item_id, Status.DONE, "Test",  DATE_FOR_USE) for item_id in range(0, 4)]
    view_model_output = ViewModel(items)

    assert view_model_output.show_all_done_items


def test_view_model_does_not_return_all_completed_tiems():
    items = [Item(item_id, Status.DONE, "Test",  DATE_FOR_USE) for item_id in range(0, 6)]
    view_model_output = ViewModel(items)

    assert not view_model_output.show_all_done_items


def test_recent_done_items_returns_items_completed_today(today, yesterday):
    item_today = Item(1, Status.DONE, "Test", today)
    item_yesterday = Item(2, Status.DONE, "Test", yesterday)

    view_model = ViewModel([item_today, item_yesterday])

    assert item_today in view_model.recent_done_items
    assert item_yesterday not in view_model.recent_done_items


def test_older_done_items_returns_items_not_completed_today(today, yesterday):
    item_today = Item(1, Status.DONE, "Test", today)
    item_yesterday = Item(2, Status.DONE, "Test", yesterday)

    view_model = ViewModel([item_today, item_yesterday])

    assert item_today not in view_model.older_done_items
    assert item_yesterday in view_model.older_done_items
