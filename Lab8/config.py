import os.path

basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'labs.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "secret"
