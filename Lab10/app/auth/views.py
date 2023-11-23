from flask import Blueprint

auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates", url_prefix="/")


@auth_bp.route('/')
def main_page():
    return "Hello, I am finally working!!!"


@auth_bp.route("/login")
def login_page():
    return "Login"


@auth_bp.route("/users")
def users_page():
    ...


@auth_bp.route("/update")
def update_page():
    ...


@auth_bp.route("/signup")
def signup_page():
    ...
