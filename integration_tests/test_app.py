import pytest
from todo_app.trello.trello_api import TrelloAPI

DATE = '2020-01-03T12:00:00Z'
DONE_ID = '5eeb34b895d54b77a6bcb8fd'
TODO_ID = '5aab34b895d54b77a6bcb8fd'

@pytest.fixture(autouse=True)
def mock_trello_get_requests(monkeypatch):
    def mock_trello_return(*args, **kwargs):
        return [
            {
                'id': '1234567',
                'dateLastActivity': DATE,
                'idList': DONE_ID,
                'name': 'DateName'
            },
            {
                'id': '1234567',
                'dateLastActivity': DATE,
                'idList': TODO_ID,
                'name': 'ToDoTask'
            }
        ]
    monkeypatch.setattr(TrelloAPI, "get_cards_from_board", mock_trello_return)

@pytest.fixture(autouse=True)
def mock_trello_get_lists(monkeypatch):
    def mock_trello_get_lists_return(*args, **kwargs):
        return [
            {
                'id': DONE_ID,
                'name': 'Done'
            },
            {
                'id': TODO_ID,
                'name': 'To Do'
            }
        ]
    monkeypatch.setattr(TrelloAPI, "_query_trello_boards", mock_trello_get_lists_return)


def test_index_page(client):
    response = client.get('/')
    assert "DateName" in str(response.get_data())
    assert "ToDoTask" in str(response.get_data())
