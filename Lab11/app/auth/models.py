from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return UserModel.query.get(str(user_id))


class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(125), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    about = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    image = db.Column(db.String(256), nullable=False, default="/default.jpg")
    last_seen = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"({self.username}, {self.email})"
