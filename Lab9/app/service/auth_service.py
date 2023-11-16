import json
from functools import wraps
from hashlib import sha256
from flask import session, redirect, url_for
from flask_login import login_user

from app import db, login_manager
from app.domain.exception import UserInputException
from app.domain.forms import ChangePassForm
from app.domain import forms
from app.domain import models
from app.domain.models import UserModel


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
        repeat_password = form.repeat_password.data

        if password != repeat_password:
            raise UserInputException("Passwords does not match!")
        if models.UserModel.query.filter_by(username=username).first():
            raise UserInputException(f"User with username {username} already exists")
        if models.UserModel.query.filter_by(email=email).first():
            raise UserInputException(f"User with email {email} already exists")

        new_user = models.UserModel(username=username, email=email)
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

    def set_session_value(self, value: str) -> None:
        session[self._SESSION_KEY] = value

    def is_pre_authorized(self) -> bool:
        return session and session.get(self._SESSION_KEY)

    @staticmethod
    def find_users():
        users = models.UserModel.query.all()
        users = map(lambda x: str(x), users)
        return list(users)

    def change_pass(self, change_pass_form: ChangePassForm) -> None:
        # TODO: change it for new db usage
        if not change_pass_form.validate():
            raise UserInputException("Form is not valid")

        old_pass = change_pass_form.old_password.data
        new_pass = change_pass_form.new_password.data
        repeat_pass = change_pass_form.repeated_password.data

        if sha256(old_pass.encode()).hexdigest() != self.credentials["password"]:
            raise UserInputException("Wrong password!!!")
        if new_pass != repeat_pass:
            raise UserInputException("New password and repeated password are not same!!!")
        if len(new_pass) < 4:
            raise UserInputException("Password must be at least 4 characters long")

        new_pass = sha256(new_pass.encode()).hexdigest()
        self.credentials["password"] = new_pass

        json_cred = json.dumps(self.credentials, indent=2)

        with open(self.json_path, "w") as f:
            f.write(json_cred)


def get_session_dict() -> dict:
    return dict(session)
