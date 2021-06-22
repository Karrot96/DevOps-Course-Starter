import os
import time
from threading import Thread

import pytest
from dotenv import load_dotenv
from dotenv.main import find_dotenv
from flask_login import utils
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from todo_app.app import create_app
from todo_app.mongo.mongo_wrapper import MongoWrapper
from todo_app.user.user import User

SELENIUM_DATABASE = "SeleniumTest"


@pytest.fixture(scope='module')
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope='module')
def test_app(monkeymodule):
    mongo_db = MongoWrapper(os.environ.get('MONGO_URL'), SELENIUM_DATABASE)
    
    def get_user():
        return User(os.environ.get("WRITER_ID"))
    monkeymodule.setattr(utils, "_get_user", get_user)

    # construct the new application
    application = create_app(SELENIUM_DATABASE)
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    mongo_db.delete_database()
    


@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver


def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    # Create new item
    input_box = driver.find_element_by_name("title")
    input_box.clear()
    input_box.send_keys("e2e_test")
    input_box.send_keys(Keys.RETURN)

    # Allow time for the API to update
    time.sleep(1)

    # Check the new item exists on the page.
    assert "e2e_test" in driver.page_source
    assert "e2e_test_ToDo" in driver.page_source

    # Check can move to in progress
    complete_button = driver.find_element_by_name("e2e_test_ToDo")
    complete_button.click()

    time.sleep(1)

    # Check the in progress item exists on the page.
    assert "e2e_test" in driver.page_source
    assert "e2e_test_Doing" in driver.page_source

    # Check can move to completed
    complete_button = driver.find_element_by_name("e2e_test_Doing")
    complete_button.click()

    time.sleep(1)

    # Check the item still exists and that the correct button shows up
    assert "e2e_test" in driver.page_source
    assert "e2e_test_Complete" in driver.page_source

    # Check can undo completed and item
    complete_button = driver.find_element_by_name("e2e_test_Complete")
    complete_button.click()

    time.sleep(1)

    # Check the item still exists and that the correct button shows up
    assert "e2e_test" in driver.page_source
    assert "e2e_test_ToDo" in driver.page_source
