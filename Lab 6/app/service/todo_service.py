from app.domain.exception import UserInputException
from app.domain.forms import TodoForm
from app.domain.models import TodoModel
from app import db


def add_todo(todo_form: TodoForm):
    if not todo_form.validate():
        raise UserInputException("TODO form input is not valid!!!!")

    try:
        task = todo_form.todo.data
        status = todo_form.status.data
        todo = TodoModel(todo=task, status=status)
        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        raise UserInputException(str(e))

    return True


def update_todo(todo_form: TodoForm, id: int):
    todo_model = TodoModel.query.get(id)

    todo_model.todo = todo_form.todo.data
    todo_model.status = todo_form.status.data
    db.session.commit()


def delete_todo(id: int):
    TodoModel.query.filter_by(id=id).delete()
    db.session.commit()
    return True
