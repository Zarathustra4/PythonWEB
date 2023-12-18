import datetime

from flask import current_app
from flask_jwt_extended import create_access_token

from app.todo.models import TodoModel, StatusEnum
from ..auth.models import UserModel
from ..exceptions import UserInputException
from ..extensions import db, jwt_manager


def model_to_dict(model: TodoModel) -> dict:
    return {
        "todo": model.todo,
        "status": model.status.name
    }


def status_str_to_enum(str_status: str) -> StatusEnum:
    for enum_status in StatusEnum:
        if enum_status.name == str_status:
            return enum_status
    raise ValueError(f"There is no such enum value - {str_status}")


def validate_data(data: dict) -> None:
    try:
        data["todo"]
    except KeyError:
        raise UserInputException("todo value is required")

    try:
        data["status"]
    except KeyError:
        raise UserInputException("status value is required")


def get_model_by_id(todo_id: int) -> TodoModel:
    todo = TodoModel.query.filter_by(id=todo_id).first()
    if todo is None:
        raise UserInputException(f"There is no todo row with such id - {todo_id}")
    return todo


def get_all_todo() -> list:
    return list(map(model_to_dict, TodoModel.query.all()))


def create_todo(data: dict) -> dict:
    validate_data(data)

    todo = data["todo"]
    status = status_str_to_enum(data["status"])
    todo_model = TodoModel(todo=todo, status=status)
    db.session.add(todo_model)
    db.session.commit()

    return model_to_dict(todo_model)


def get_todo_by_id(todo_id: int) -> dict:
    todo = get_model_by_id(todo_id)
    return model_to_dict(todo)


def update_todo(todo_id: int, data: dict) -> dict:
    validate_data(data)
    todo_model = get_model_by_id(todo_id)

    todo_model.todo = data['todo']
    todo_model.status = data["status"]

    db.session.commit()

    return model_to_dict(todo_model)


def delete_todo(todo_id: int) -> dict:
    TodoModel.query.filter_by(id=todo_id).delete()
    db.session.commit()
    return {"message": "The todo record was deleted"}


def generate_token(username: str, password):
    auth_message = "Wrong username or password"
    user = UserModel.query.filter_by(username=username).first()
    if user is None:
        raise UserInputException(auth_message)
    if not user.check_password(password):
        raise UserInputException(auth_message)

    return create_access_token(identity=username)
