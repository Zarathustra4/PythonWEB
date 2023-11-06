from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = b"secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db.init_app(app)

migrate = Migrate(app, db, command='migrate')

from app import views
