from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user

from app.auth import forms, service
from app.exceptions import UserInputException

auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates", url_prefix="/")


@auth_bp.route('/')
@login_required
def main_page():
    user = current_user
    return render_template("account.html", current_user=user)


@auth_bp.route("/login", methods=["POST"])
def login():
    login_form = forms.LoginForm()
    if not login_form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("auth_bp.login_page"))

    try:
        service.authenticate(login_form)
        flash("You were successfully logged in", category="message")
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for("auth_bp.login_page"))

    return redirect(url_for("auth_bp.main_page"))


@auth_bp.route("/login", methods=["GET"])
def login_page():
    login_form = forms.LoginForm()
    return render_template("login.html", form=login_form, unauthorized=True)


@auth_bp.route("/users", methods=["GET"])
@login_required
def users_page():
    users = service.find_users()
    return render_template('users.html',
                           users_list=users,
                           total_users=len(users))


@auth_bp.route("/signup")
def signup_page():
    form = forms.RegisterForm()
    return render_template("signup.html", form=form, unauthorized=True)


@auth_bp.route("/sign-up", methods=["POST"])
def signup():
    form = forms.RegisterForm()
    if not form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("auth_bp.signup_page"))
    try:
        service.create_user(form)
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for('auth_bp.signup_page'))
    else:
        flash("User was successfully created")
    return redirect(url_for('auth_bp.main_page'))


@auth_bp.route("/update", methods=["GET"])
@login_required
def update_page():
    user = current_user
    form = forms.UpdateForm(username=user.username, email=user.email, about=user.about)
    return render_template("update.html", form=form)


@auth_bp.route("/update", methods=["POST"])
@login_required
def update():
    form = forms.UpdateForm()
    user_id = current_user.id
    if not form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("auth_bp.main_page"))

    try:
        service.update_user(form, user_id)
    except UserInputException as e:
        flash(str(e), category='message')
    else:
        flash("User data was successfully updated")

    return redirect(url_for("auth_bp.main_page"))


@auth_bp.route("/change-password", methods=["GET"])
@login_required
def change_password_page():
    form = forms.ChangePassForm()
    return render_template("change-password.html", form=form)


@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    change_pass_form = forms.ChangePassForm()
    user = current_user
    try:
        service.change_pass(user, change_pass_form)
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for("auth_bp.change_password_page"))

    flash("The password was successfully changed", category="message")
    return redirect(url_for("auth_bp.main_page"))


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))
