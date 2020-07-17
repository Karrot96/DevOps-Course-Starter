from dateutil import parser


class Item:
    def __init__(self, id, complete, title, last_updated):
        self.id = id
        self.completed = complete
        self.title = title
        self.last_updated = parser.isoparse(last_updated).replace(tzinfo=None)

    def __repr__(self):
        return f"(id: {self.id}, completed: {self.completed}, title: {self.title})"

    def add_url(self, url):
        self.url = url
        return self