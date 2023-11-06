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
