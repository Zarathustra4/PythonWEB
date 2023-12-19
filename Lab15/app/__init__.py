from flask import Flask

from .api_user.res import users_api
from .extensions import db, migrate, login_manager, jwt_manager

from config import config
from app.auth.views import auth_bp
from app.todo.views import todo_bp
from app.cookies.views import cookies_bp
from app.about.views import about_bp
from app.assigment.views import assigment_bp
from app.posts.views import posts_bp
from app.todo_api.routes import todo_api
from app.swagger.docs import swagger_bp


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config.get(config_name))

    from app.auth import models
    from app.todo import models
    from app.assigment import models
    from app.posts import models

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(auth_bp)
        app.register_blueprint(about_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(cookies_bp)
        app.register_blueprint(assigment_bp)
        app.register_blueprint(posts_bp)
        app.register_blueprint(todo_api)
        app.register_blueprint(users_api)
        app.register_blueprint(swagger_bp)

    return app
