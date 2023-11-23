from flask import Flask
from .extensions import db, migrate

from config import config
from app.auth.views import auth_bp


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config.get(config_name))

    from app.auth import models

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        app.register_blueprint(auth_bp)

    return app
