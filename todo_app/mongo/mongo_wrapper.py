from datetime import datetime
from todo_app.models.item import Item, Status
import pymongo
from bson.objectid import ObjectId
import os


class MongoWrapper:

    def __init__(self, database: str = ""):
        
        client = self._connect(database)
        self.db = client.database

    def _connect(self, database):
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        mongo_url = os.environ['MONGO_URL']
        return pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{mongo_url}/{database}?w=majority")

    def _move_card_lists(self, id, new_list, old_list):
        post = old_list.find_one({"_id": ObjectId(id)})
        post["dateLastActivity"] = datetime.utcnow()
        new_list.insert_one(post)
        old_list.delete_one({"_id": ObjectId(id)})

    def delete_database(self):
        self.db.todo.drop()
        self.db.completed.drop()
        self.db.doing.drop()

    def create_database(cls, name: str) -> "MongoWrapper":
        return MongoWrapper(name)

    def _get_items_from_collection(self, collection):
        return collection.find()

    def _get_lists_from_db(self):
        todo_list = self.db.todo
        completed_list = self.db.completed
        doing_list = self.db.doing
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
