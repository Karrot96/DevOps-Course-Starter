from todo_app.user.user import User
import pytest
from dotenv import find_dotenv, load_dotenv
from todo_app.app import create_app
from todo_app.mongo.mongo_wrapper import MongoWrapper
import mongomock
from todo_app.github.github_authentication import GithubAuthentication
from flask_login import utils
import os

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(MongoWrapper, "_connect", mongomock.MongoClient)
    # Use our test integration config instead of the 'real' version
    try:
        file_path = find_dotenv('todo_app/.env.test')
        load_dotenv(file_path, override=False)
    except OSError:
        # Often we can just ignore this error as it means we already have the variables set
        pass
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client
