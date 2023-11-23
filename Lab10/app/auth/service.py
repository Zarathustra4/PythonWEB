import datetime
import os

from flask_login import login_user
from werkzeug.utils import secure_filename

from .forms import ChangePassForm
from .models import UserModel
from ..extensions import db
from app.auth import forms, models
from app.exceptions import UserInputException
import config


def find_users():
    users = models.UserModel.query.all()
    users = map(lambda x: str(x), users)
    return list(users)


def create_user(form: forms.RegisterForm):
    username = form.username.data
    email = form.email.data
    password = form.password.data
    about = form.about.data
    image = form.image.data

    if models.UserModel.query.filter_by(username=username).first():
        raise UserInputException(f"User with username {username} already exists")
    if models.UserModel.query.filter_by(email=email).first():
        raise UserInputException(f"User with email {email} already exists")

    filename = secure_filename(image.filename)
    image.save(os.path.join(
        config.basedir, 'app', 'static', 'images', filename
    ))

    new_user = models.UserModel(username=username, email=email, image=filename,
                                about=about, last_seen=datetime.datetime.now().date())
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)


def authenticate(form: forms.LoginForm):
    username = form.login.data
    password = form.password.data
    remember = form.remember.data

    user: models.UserModel = models.UserModel.query.filter_by(username=username).first()
    if not user:
        raise UserInputException(f"No such a user with username {username}")

    if user.check_password(password):
        login_user(user, remember=remember)
    else:
        raise UserInputException("Wrong username of password")

    user.last_seen = datetime.datetime.now().date()
    db.session.commit()


def update_validate(user: UserModel, email: str, username: str) -> str:
    if user.email != email and UserModel.query.filter_by(email=email).first():
        return "The email is already taken"
    if user.username != username and UserModel.query.filter_by(username=username).first():
        return "The username is already taken"
    return ""


def update_user(form: forms.UpdateForm, user_id: int):
    username = form.username.data
    email = form.email.data
    about = form.about.data
    image = form.image.data
    user = UserModel.query.filter_by(id=user_id).first()
    validation_msg = update_validate(user, email, username)
    if validation_msg:
        raise UserInputException(validation_msg)
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(
            config.basedir, 'app', 'static', 'images', filename
        ))
    else:
        filename = user.image
    user.username = username
    user.email = email
    user.image = filename
    user.about = about
    db.session.commit()


def change_pass(user: UserModel, change_pass_form: ChangePassForm) -> None:
    # TODO: change it for new db usage
    if not change_pass_form.validate():
        raise UserInputException("Form is not valid")
    old_pass = change_pass_form.old_password.data
    new_pass = change_pass_form.new_password.data
    if not user.check_password(old_pass):
        raise UserInputException("Wrong password")
    user.set_password(new_pass)
    db.session.commit()
