import os
from threading import Thread
from trello.trello_api import TrelloAPI
import app
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    trello_board = TrelloAPI().create_board("SeleniumTest")
    os.environ['TRELLO_BOARD_ID'] = trello_board.board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    trello_board.delete_trello_board()


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
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