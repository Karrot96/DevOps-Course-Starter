from todo_app.app import create_app
from todo_app.user.user import User
import pytest
from todo_app.mongo.mongo_wrapper import MongoWrapper
import mongomock

DATE = '2020-01-03T12:00:00Z'
DONE_ID = '5eeb34b895d54b77a6bcb8fd'
TODO_ID = '5aab34b895d54b77a6bcb8fd'


@pytest.fixture(autouse=True)
def mock_db_init(monkeypatch):
    def mock_mongo_return(*args, **kwargs):
        todo_collection = mongomock.MongoClient().test.todo
        doing_collection = mongomock.MongoClient().test.doing
        completed_collection = mongomock.MongoClient().test.completed
        todo_collection.insert_one({
            '_id': '1234567',
            'dateLastActivity': DATE,
            'name': 'ToDoTask'
        })
        completed_collection.insert_one({
            '_id': '1234567',
            'dateLastActivity': DATE,
            'name': 'DateName'
        })
        return ( todo_collection, completed_collection, doing_collection)
    monkeypatch.setattr(MongoWrapper, "_get_lists_from_db", mock_mongo_return)


def test_index_page(client):
    response = client.get('/')
    assert "DateName" in str(response.get_data())
    assert "ToDoTask" in str(response.get_data())
