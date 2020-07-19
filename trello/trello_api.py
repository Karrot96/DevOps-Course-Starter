import requests
import json
from Models.item import Item


class TrelloAPI:

    def __init__(self, board_id):
        with open("secrets/trello_secrets.json", "r") as json_file:
            data = json.load(json_file)
            self.key = data["key"]
            self.token = data["token"]
        self.board_id = board_id

    def _get_query(self, **kwargs):
        query = {
            "key": self.key,
            "token": self.token,
            **kwargs
        }
        for key, value in kwargs.items():
            query[key] = value
        return query

    def _move_card_lists(self, id, list_id):
        url = f"https://api.trello.com/1/cards/{id}"
        headers = {
            "Accept": "application/json"
        }
        response = requests.request(
            "PUT",
            url,
            headers=headers,
            params=self._get_query(idList=list_id)
        )

    def _query_trello_boards(self, endpoint, **kwargs):
        url = f"https://api.trello.com/1/boards/{self.board_id}/{endpoint}"
        headers = {
            "Accept": "application/json"
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=self._get_query(**kwargs)
        )

        return (response.json())

    def get_cards_from_board(self):
        return self._query_trello_boards("cards")

    def _get_lists_from_board(self):
        lists = self._query_trello_boards("lists")
        todo_list_id = ""
        completed_list_id = ""
        for list_items in lists:
            if list_items["name"] == "Not Started":
                todo_list_id = list_items["id"]
                continue
            if list_items["name"] == "Completed":
                completed_list_id = list_items["id"]
                continue
        return todo_list_id, completed_list_id

    def get_items(self):
        todo_list_id, completed_list_id = self._get_lists_from_board()
        items = []
        for card in self.get_cards_from_board():
            if card["idList"] == todo_list_id:
                complete = False
            elif card["idList"] == completed_list_id:
                complete = True
            else:
                raise ValueError(f"{card['name']} is not a member of a valid Todo list")
            items.append(Item(card["id"], complete, card["name"], card["dateLastActivity"]))
        return items

    def add_item(self, title):
        todo_list_id, _ = self._get_lists_from_board()
        url = "https://api.trello.com/1/cards"
        response = requests.request(
            "POST",
            url,
            params=self._get_query(idList=todo_list_id, name=title)
        )

    def complete_item(self, id):
        _, completed_list_id = self._get_lists_from_board()
        self._move_card_lists(id, completed_list_id)

    def set_todo(self, id):
        todo_list_id, _ = self._get_lists_from_board()
        self._move_card_lists(id, todo_list_id)