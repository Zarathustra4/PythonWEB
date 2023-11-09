from app import db, app
from enum import Enum


class StatusEnum(Enum):
    TODO = "To Do"
    PROGRESS = "In Progress"
    DONE = "Done"


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEnum))

