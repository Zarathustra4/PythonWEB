from app import db
from enum import Enum


class StatusEnum(Enum):
    TODO = "To Do"
    PROGRESS = "In Progress"
    DONE = "Done"


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEnum))


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(125), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(125), nullable=False, default="default.jpg")
    password = db.Column(db.String(125), nullable=False)

    def __repr__(self):
        return f"( {self.username}, {self.email} )"
