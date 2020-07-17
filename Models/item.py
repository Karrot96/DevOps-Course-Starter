
class Item:
    def __init__(self, id, complete, title):
        self.id = id
        self.completed = complete
        self.title = title

    def __repr__(self):
        return f"(id: {self.id}, completed: {self.completed}, title: {self.title})"

    def add_url(self, url):
        self.url = url
        return self