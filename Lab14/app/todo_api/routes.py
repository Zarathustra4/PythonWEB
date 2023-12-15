from flask import Blueprint, request

from app.exceptions import UserInputException
from app.todo_api import service

todo_api = Blueprint("todo_api", __name__,
                     template_folder="templates", url_prefix="/api/todos")


@todo_api.route("/", methods=["GET"])
def get_todo_list():
    return service.get_all_todo()


@todo_api.route("/", methods=["POST"])
def post_todo():
    data = request.json
    try:
        return service.create_todo(data)
    except UserInputException as e:
        return {"message": str(e)}, 400


@todo_api.route("/<int:todo_id>", methods=["GET"])
def get_todo(todo_id: int):
    try:
        return service.get_todo_by_id(todo_id)
    except UserInputException as e:
        return {"message": str(e)}, 400


@todo_api.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id: int):
    data = request.json
    try:
        return service.update_todo(todo_id, data)
    except UserInputException as e:
        return {"message": str(e)}, 400


@todo_api.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id: int):
    try:
        return service.delete_todo(todo_id)
    except UserInputException as e:
        return {"message": str(e)}, 400
