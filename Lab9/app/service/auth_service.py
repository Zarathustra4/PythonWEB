import datetime
import json
import os
from functools import wraps
from hashlib import sha256
from flask import session, redirect, url_for
from flask_login import login_user

import config
from app import db, login_manager, app
from app.domain.exception import UserInputException
from app.domain.forms import ChangePassForm
from app.domain import forms
from app.domain import models
from app.domain.models import UserModel
from werkzeug.utils import secure_filename


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)


class AuthService:
    def __init__(self):
        self._SESSION_KEY = "user_login"

    def create_user(self, form: forms.RegisterForm):
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

    def authenticate(self, form: forms.LoginForm):
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


    def set_session_value(self, value: str) -> None:
        session[self._SESSION_KEY] = value

    def is_pre_authorized(self) -> bool:
        return session and session.get(self._SESSION_KEY)

    @staticmethod
    def find_users():
        users = models.UserModel.query.all()
        users = map(lambda x: str(x), users)
        return list(users)

    def update_validate(self, user: UserModel, email: str, username: str) -> str:
        if user.email != email and UserModel.query.filter_by(email=email).first():
            return "The email is already taken"
        if user.username != username and UserModel.query.filter_by(username=username).first():
            return "The username is already taken"
        return ""

    def update_user(self, form: forms.UpdateForm, user_id: int):
        username = form.username.data
        email = form.email.data
        about = form.about.data
        image = form.image.data

        user = UserModel.query.filter_by(id=user_id).first()

        validation_msg = self.update_validate(user, email, username)
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

    def change_pass(self, user: UserModel, change_pass_form: ChangePassForm) -> None:
        # TODO: change it for new db usage
        if not change_pass_form.validate():
            raise UserInputException("Form is not valid")

        old_pass = change_pass_form.old_password.data
        new_pass = change_pass_form.new_password.data

        if not user.check_password(old_pass):
            raise UserInputException("Wrong password")

        user.set_password(new_pass)
        db.session.commit()


def get_session_dict() -> dict:
    return dict(session)
