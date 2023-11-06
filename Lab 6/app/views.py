from app import app
from app.domain.models import TodoModel
from app.service.auth_service import AuthService
from app.service.auth_service import get_session_dict
from app.domain.exception import UserInputException
from flask import render_template, request, redirect, url_for, session, flash
import platform
import datetime
from app.domain.forms import LoginForm, ChangePassForm, TodoForm
from app.service.todo_service import add_todo


SKILLS = ["C++", "Python", "Java", "Spring", "Math", "SQL", "REST API", "Git", "Linux", "HTML/CSS"]
auth_service = AuthService()

pre_authorized = auth_service.get_pre_login_decorator()


@app.route("/")
@pre_authorized
def main_page():
    return render_template("index.html",
                           cookies=get_session_dict(),
                           user_login=auth_service.get_session_key(),
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/hobbies")
@pre_authorized
def hobbies_page():
    return render_template("hobbies.html")


@app.route("/study")
@pre_authorized
def study_page():
    return render_template("studying.html")


@app.route("/skills")
@app.route("/skills/<int:id>")
@pre_authorized
def skills_page(id=None):
    is_list = True
    if id:
        skills = SKILLS[id:id + 1] if 0 <= id < len(SKILLS) else ["Wrong index!!!"]
        is_list = False
    else:
        skills = SKILLS

    return render_template("skills.html",
                           len=len(skills),
                           is_list=is_list,
                           skills=skills)


@app.route("/login", methods=['GET'])
def login_page():
    login_form = LoginForm()
    return render_template("login.html", form=login_form)


@app.route("/login", methods=['POST'])
def login():
    login_form = LoginForm()
    if not login_form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("login_page"))

    login_input = login_form.login.data
    password_input = login_form.password.data
    remember_input = login_form.remember.data

    if auth_service.authenticate(login_input, password_input):
        auth_service.set_session_value(value=login_input)
        flash("You were successfully logged in", category="message")
        return redirect(url_for("main_page")) if not remember_input else redirect(url_for("skills_page"))

    flash("Wrong login or password", category="error")
    return redirect(url_for("login_page"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/cookie", methods=["POST"])
def post_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    session[key] = value
    return redirect(url_for("main_page"))


@app.route("/cookie/delete/<key>", methods=["POST"])
@app.route("/cookie/delete", methods=["POST"])
def delete_cookie(key=None):
    if key:
        session.pop(key)
    else:
        session.clear()
    return redirect(url_for("main_page"))


@app.route("/change-password", methods=["GET"])
@pre_authorized
def change_password_page():
    form = ChangePassForm()
    return render_template("change-password.html", form=form)


@app.route("/change-password", methods=["POST"])
def change_password():
    change_pass_form = ChangePassForm()
    if not change_pass_form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("change_password_page"))

    old_pass = change_pass_form.old_password.data
    new_pass = change_pass_form.new_password.data
    repeat_pass = change_pass_form.repeated_password.data

    try:
        auth_service.change_pass(old_pass, new_pass, repeat_pass)
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for("change_password_page"))

    flash("The password was successfully changed", category="message")
    return redirect(url_for("main_page"))


@app.route("/todo", methods=['GET'])
def todo_page():
    todo_form = TodoForm()
    todo_list = TodoModel.query.all()
    return render_template('todo.html', form=todo_form, todo_list=todo_list)


@app.route("/todo", methods=['POST'])
def create_todo():
    todo_form = TodoForm()
    try:
        add_todo(todo_form)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo was successfully addded!")

    return redirect(url_for("todo_page"))
