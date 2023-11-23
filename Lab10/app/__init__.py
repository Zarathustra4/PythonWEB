from flask import Flask
from .extensions import db, migrate, login_manager

from config import config
from app.auth.views import auth_bp
from app.todo.views import todo_bp
from app.cookies.views import cookies_bp
from app.about.views import about_bp
from app.assigment.views import assigment_bp


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config.get(config_name))

    from app.auth import models
    from app.todo import models

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(auth_bp)
        app.register_blueprint(about_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(cookies_bp)
        app.register_blueprint(assigment_bp)

    return app
