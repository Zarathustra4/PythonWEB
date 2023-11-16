from flask_login import UserMixin

from app import db
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class StatusEnum(Enum):
    TODO = "To Do"
    PROGRESS = "In Progress"
    DONE = "Done"


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEnum))


class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(125), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"({self.username}, {self.email})"

