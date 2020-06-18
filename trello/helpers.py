import requests
import json

class Trello:

    key = ""
    token = ""

    def __init__(self):
        with open("secrets/trello_secrets.json", "r") as json_file:
            data = json.load(json_file)
            self.key = data["key"]
            self.token = data["token"]

    def get_query(self, **kwargs):
        query = {
            "key": self.key,
            "token": self.token
        }
        for key, value in kwargs.items():
            query[key] = value
        return query

    def get_all_cards_from_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        headers = {
        "Accept": "application/json"
        }
        response = requests.request(
        "GET",
        url,
        headers=headers,
        params=self.get_query()
        )

        print(response.json())


if __name__ == "__main__":
    trello_api = Trello()
    print(trello_api.get_all_cards_from_board("6yxcx50y"))