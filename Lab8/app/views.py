from flask_login import login_required

from app import app, login_manager
from app.domain.models import TodoModel
from app.service.auth_service import AuthService
from app.service.auth_service import get_session_dict
from app.domain.exception import UserInputException
from flask import render_template, request, redirect, url_for, session, flash
import platform
import datetime
import app.domain.forms as forms
from app.service.todo_service import add_todo, update_todo, delete_todo

# TODO: Make normal templates structure
SKILLS = ["C++", "Python", "Java", "Spring", "Math", "SQL", "REST API", "Git", "Linux", "HTML/CSS"]
auth_service = AuthService()

pre_authorized = auth_service.get_pre_login_decorator()
login_manager.login_view = 'login_page'


@app.route("/")
@login_required
def main_page():
    return render_template("index.html",
                           cookies=get_session_dict(),
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/hobbies")
@login_required
def hobbies_page():
    return render_template("hobbies.html")


@app.route("/study")
@login_required
def study_page():
    return render_template("studying.html")


@app.route("/skills")
@app.route("/skills/<int:id>")
@login_required
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
    login_form = forms.LoginForm()
    return render_template("login.html", form=login_form)


@app.route("/login", methods=['POST'])
def login():
    login_form = forms.LoginForm()
    if not login_form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("login_page"))

    try:
        auth_service.authenticate(login_form)
        flash("You were successfully logged in", category="message")
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for("login_page"))

    return redirect(url_for("main_page"))


@app.route("/logout", methods=["POST"])
@login_required
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
@login_required
def change_password_page():
    form = forms.ChangePassForm()
    return render_template("change-password.html", form=form)


@app.route("/change-password", methods=["POST"])
def change_password():
    change_pass_form = forms.ChangePassForm()

    try:
        auth_service.change_pass(change_pass_form)
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for("change_password_page"))

    flash("The password was successfully changed", category="message")
    return redirect(url_for("main_page"))


@app.route("/todo", methods=['GET'])
@login_required
def todo_page():
    todo_form = forms.TodoForm()
    todo_list = TodoModel.query.all()
    return render_template('todo.html', form=todo_form, todo_list=todo_list)


@app.route("/todo", methods=['POST'])
def create_todo():
    todo_form = forms.TodoForm()
    try:
        add_todo(todo_form)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo was successfully addded!")

    return redirect(url_for("todo_page"))


@app.route("/todo/update/<int:id>", methods=["GET"])
@login_required
def todo_update_page(id: int):
    try:
        todo_model = TodoModel.query.get(id)
    except Exception as e:
        flash(str(e), category="error")
        return redirect(url_for('todo_page'))
    todo_form = forms.TodoForm()
    todo_form.todo.data = todo_model.todo
    todo_form.status.data = todo_model.status
    todo_form.submit.label.text = 'Update'

    return render_template("todo_update.html", id=id, form=todo_form)


@app.route("/todo/update/<int:id>", methods=["POST"])
def todo_update(id: int):
    todo_form = forms.TodoForm()
    try:
        update_todo(todo_form, id)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo task is updated")
    finally:
        return redirect(url_for("todo_page"))


@app.route("/todo/delete/<int:id>", methods=["POST"])
def todo_delete(id: int):
    try:
        delete_todo(id)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo task is deleted")
    finally:
        return redirect(url_for("todo_page"))


@app.route("/sign-up", methods=["GET"])
@login_required
def signup_page():
    form = forms.RegisterForm()
    return render_template("signup.html", form=form)


@app.route("/sign-up", methods=["POST"])
def signup():
    form = forms.RegisterForm()
    if not form.validate():
        flash("Form is not valid", category="error")
        return redirect(url_for("signup_page"))
    try:
        auth_service.create_user(form)
    except UserInputException as e:
        flash(str(e), category="error")
        return redirect(url_for('signup_page'))
    else:
        flash("User was successfully created")
    return redirect(url_for('main_page'))


@app.route("/users", methods=["GET"])
@login_required
def users_page():
    users = AuthService.find_users()
    return render_template('users.html',
                           users_list=users,
                           total_users=len(users))
