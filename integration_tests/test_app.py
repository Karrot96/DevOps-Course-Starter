import pytest
from trello.trello_api import TrelloAPI

DATE = "2020-01-03T12:00:00Z"
COMPLETED_ID = "5eeb34b895d54b77a6bcb8fd"
TODO_ID = "5aab34b895d54b77a6bcb8fd"

@pytest.fixture(autouse=True)
def mock_trello_get_requests(monkeypatch):
    def mock_trello_return(*args, **kwargs):
        return [{
            {
                'id': "1234567",
                'dateLastActivity': DATE,
                'idList': COMPLETED_ID,
                'name': "DateName"
            }
        }]
    monkeypatch.setattr(TrelloAPI, "get_cards_from_board", mock_trello_return)

@pytest.fixture(autouse=True)
def mock_trello_get_lists(monkeypatch):
    def mock_trello_get_lists_return(*args, **kwargs):
        return [
            {
                'id': COMPLETED_ID,
                'name': 'Completed'
            },
            {
                'id': TODO_ID,
                'name': 'Not Started'
            }
        ]
    monkeypatch.setattr(TrelloAPI, "_query_trello_boards", mock_trello_get_lists_return)


def test_index_page(client):
    response = client.get('/')
    print(response)
