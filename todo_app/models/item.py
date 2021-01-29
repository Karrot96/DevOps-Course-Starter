from enum import Enum


class Status(Enum):
    TODO = "Todo"
    DOING = "Doing"
    DONE = "Done"


class Item:
    def __init__(self, id, complete, title, last_updated):
        self.id = id
        self.status: Status = complete
        self.title = title
        self.last_updated = last_updated

    def __repr__(self):
        return f"(id: {self.id}, status: {self.status.name}, title: {self.title})"

    def add_url(self, url):
        self.url = url
        return self
