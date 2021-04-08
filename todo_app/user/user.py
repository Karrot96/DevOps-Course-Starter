from flask_login.mixins import UserMixin
from enum import Enum
import os


class Roles(Enum):
    WRITER = 1
    READER = 2


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = Roles.WRITER if self.id == os.environ.get("WRITER_ID") else Roles.READER
    
    def check_role(self, level: Roles) -> bool:
        return self.role == level