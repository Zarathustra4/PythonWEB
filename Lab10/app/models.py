from enum import Enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

class StatusEnum(Enum):
    TODO = "To Do"
    PROGRESS = "In Progress"
    DONE = "Done"


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEnum))
