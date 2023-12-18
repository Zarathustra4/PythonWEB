from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.exceptions import UserInputException
from app.todo_api import service

todo_api = Blueprint("todo_api", __name__,
                     template_folder="templates", url_prefix="/api/todos")


@todo_api.route("/", methods=["GET"])
@jwt_required()
def get_todo_list():
    return jsonify(service.get_all_todo())


@todo_api.route("/", methods=["POST"])
@jwt_required()
def post_todo():
    data = request.json
    try:
        return jsonify(service.create_todo(data))
    except UserInputException as e:
        return jsonify({"message": str(e)}), 400


@todo_api.route("/<int:todo_id>", methods=["GET"])
@jwt_required()
def get_todo(todo_id: int):
    try:
        return jsonify(service.get_todo_by_id(todo_id))
    except UserInputException as e:
        return jsonify({"message": str(e)}), 400


@todo_api.route("/<int:todo_id>", methods=["PUT"])
@jwt_required()
def update_todo(todo_id: int):
    data = request.json
    try:
        return jsonify(service.update_todo(todo_id, data))
    except UserInputException as e:
        return jsonify({"message": str(e)}), 400


@todo_api.route("/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id: int):
    try:
        return jsonify(service.delete_todo(todo_id))
    except UserInputException as e:
        return jsonify({"message": str(e)}), 400


@todo_api.route("/token", methods=["GET"])
def get_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    try:
        token = service.generate_token(username, password)
    except UserInputException as e:
        return jsonify({"message": str(e)})
    else:
        return jsonify({"token": token})

