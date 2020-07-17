from Models.view_model import ViewModel
from Models import view_model
from Models.item import Item
import pytest


@pytest.fixture(autouse=True)
def mock_response_url_for(monkeypatch):
    def mock_url_for(*args, **kwargs):
        return kwargs
    monkeypatch.setattr(view_model, "url_for", mock_url_for)


@pytest.fixture
def uncompleted_item():
    return  Item(1, False, "Item1")

@pytest.fixture
def completed_item():
    return Item(2, True, "Item2")


def test_view_model_returns_all_items(monkeypatch, completed_item, uncompleted_item):
    items = [
        uncompleted_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item in view_model_output.items
    assert completed_item in view_model_output.items


def test_view_model_returns_only_completed_items(monkeypatch, completed_item, uncompleted_item):
    items = [
        uncompleted_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item not in view_model_output.completed_items
    assert completed_item in view_model_output.completed_items


def test_view_model_returns_only_uncompleted_items(monkeypatch, completed_item, uncompleted_item):
    items = [
        uncompleted_item,
        completed_item
    ]
    view_model_output = ViewModel(items)

    assert uncompleted_item in view_model_output.uncompleted_items
    assert completed_item not in view_model_output.uncompleted_items
