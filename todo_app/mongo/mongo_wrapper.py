from datetime import datetime
from todo_app.models.item import Item, Status
import pymongo
from bson.objectid import ObjectId

TODO_BASE = "_todo"
COMPLETED_BASE = "_completed"
DOING_BASE = "_doing"

class MongoWrapper:

    def __init__(self, connection_string, database):
        client = self._connect(connection_string)
        self.db = client.database
        self.todo = self.db[f"{database}{TODO_BASE}"]
        self.completed = self.db[f"{database}{COMPLETED_BASE}"]
        self.doing = self.db[f"{database}{DOING_BASE}"]

    def _connect(self, database):
        return pymongo.MongoClient(database)

    def _move_card_lists(self, id, new_list, old_list):
        post = old_list.find_one({"_id": ObjectId(id)})
        post["dateLastActivity"] = datetime.utcnow()
        new_list.insert_one(post)
        old_list.delete_one({"_id": ObjectId(id)})

    def delete_database(self):
        self.todo.drop()
        self.completed.drop()
        self.doing.drop()

    def _get_items_from_collection(self, collection):
        return collection.find()

    def _get_lists_from_db(self):
        todo_list = self.todo
        completed_list = self.completed
        doing_list = self.doing
        return todo_list, completed_list, doing_list

    def get_items(self):
        todo_list, completed_list, doing_list = self._get_lists_from_db()
        items = []
        for item in self._get_items_from_collection(todo_list):
            items.append(Item(str(item["_id"]), Status.TODO, item["name"], item["dateLastActivity"]))
        for item in self._get_items_from_collection(doing_list):
            items.append(Item(str(item["_id"]), Status.DOING, item["name"], item["dateLastActivity"]))
        for item in self._get_items_from_collection(completed_list):
            items.append(Item(str(item["_id"]), Status.DONE, item["name"], item["dateLastActivity"]))
        return items

    def add_item(self, title):
        todo_list, _, _= self._get_lists_from_db()
        post = {
            "name": title,
            "dateLastActivity": datetime.utcnow()
        }
        todo_list.insert_one(post)

    def complete_item(self, id):
        _, completed_list, doing_list = self._get_lists_from_db()
        self._move_card_lists(id, completed_list, doing_list)

    def set_doing(self, id):
        todo_list, _, doing_list = self._get_lists_from_db()
        self._move_card_lists(id, doing_list, todo_list)

    def set_todo(self, id):
        todo_list, completed_list, _ = self._get_lists_from_db()
        self._move_card_lists(id, todo_list, completed_list)
