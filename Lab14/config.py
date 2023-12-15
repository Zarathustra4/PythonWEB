import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    WTF_CSRF_ENABLED = True
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = 'secret'
    FLASK_SECRET = SECRET_KEY


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "labs.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "labs.sqlite")


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}
