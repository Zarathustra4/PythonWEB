from enum import Enum

from ..extensions import db


class StatusEnum(Enum):
    TODO = "To Do"
    PROGRESS = "In Progress"
    DONE = "Done"


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEnum))
