import json
from functools import wraps
from hashlib import sha256
from flask import session, request, redirect, url_for, g

"""
The password is encrypted by sha256 algorithm
"""


def parse_json():
    json_path = "app/static/json/credentials.json"
    with open(json_path) as json_file:
        credentials = json.load(json_file)

    return credentials


class AuthService:
    def __init__(self):
        self.credentials = parse_json()
        self._SESSION_KEY = "user_login"

    def authenticate(self, login: str, password: str) -> bool:
        password = sha256(password.encode()).hexdigest()

        if login == self.credentials["login"] and password == self.credentials["password"]:
            return True
        return False

    def set_session_value(self, value: str) -> None:
        session[self._SESSION_KEY] = value

    def is_pre_authorized(self):
        if not session:
            return False
        if session[self._SESSION_KEY] == self.credentials["login"]:
            return True
        return False

    def get_pre_login_decorator(self):
        def login_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.is_pre_authorized():
                    return redirect(url_for('login_page'))
                return f(*args, **kwargs)

            return decorated_function

        return login_required


if __name__ == "__main__":
    print(parse_json())
