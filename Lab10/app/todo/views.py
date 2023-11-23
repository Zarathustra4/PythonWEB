from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from app.exceptions import UserInputException
from app.todo import forms, service
from app.todo.models import TodoModel

todo_bp = Blueprint("todo_bp", __name__,
                    template_folder="templates", url_prefix="/todo")


@todo_bp.route("/", methods=["GET"])
@login_required
def todo_page():
    todo_form = forms.TodoForm()
    todo_list = TodoModel.query.all()
    return render_template('todo.html', form=todo_form, todo_list=todo_list)


@todo_bp.route("/", methods=["POST"])
@login_required
def create_todo():
    todo_form = forms.TodoForm()
    try:
        service.add_todo(todo_form)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo was successfully addded!")

    return redirect(url_for("todo_bp.todo_page"))


@todo_bp.route("/update/<int:id>", methods=["GET"])
@login_required
def todo_update_page(id: int):
    try:
        todo_model = TodoModel.query.get(id)
    except Exception as e:
        flash(str(e), category="error")
        return redirect(url_for('todo_bp.todo_page'))
    todo_form = forms.TodoForm()
    todo_form.todo.data = todo_model.todo
    todo_form.status.data = todo_model.status
    todo_form.submit.label.text = 'Update'

    return render_template("todo_update.html", id=id, form=todo_form)


@todo_bp.route("/update/<int:id>", methods=["POST"])
@login_required
def todo_update(id: int):
    todo_form = forms.TodoForm()
    try:
        service.update_todo(todo_form, id)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo task is updated")
    finally:
        return redirect(url_for("todo_bp.todo_page"))


@todo_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def todo_delete(id: int):
    try:
        service.delete_todo(id)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("Todo task is deleted")
    finally:
        return redirect(url_for("todo_bp.todo_page"))
