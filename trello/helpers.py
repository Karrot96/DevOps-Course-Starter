import requests
import json

class Trello:

    key = ""
    token = ""

    def __init__(self, board_id):
        with open("secrets/trello_secrets.json", "r") as json_file:
            data = json.load(json_file)
            self.key = data["key"]
            self.token = data["token"]
        self.board_id = board_id

    def _get_query(self, **kwargs):
        query = {
            "key": self.key,
            "token": self.token
        }
        for key, value in kwargs.items():
            query[key] = value
        return query

    def _query_trell_boards(self, endpoint, **kwargs):
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
        print(self._query_trell_boards("cards"))

    def get_lists_from_board(self):
        print(self._query_trell_boards("lists"))

if __name__ == "__main__":
    trello_api = Trello("6yxcx50y")
    trello_api.get_cards_from_board()
    trello_api.get_lists_from_board()