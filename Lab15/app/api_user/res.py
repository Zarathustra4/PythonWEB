from flask import jsonify, Blueprint, request
from flask_restful import Resource, Api

from . import service
from ..exceptions import UserInputException

users_api = Blueprint("users_api", __name__, template_folder="templates", url_prefix="/api/users")
api = Api(users_api)


class Users(Resource):
    def get(self):
        return jsonify(service.find_all())

    def post(self):
        body = request.json
        try:
            user = service.create_user(body)
        except UserInputException as e:
            return jsonify({"msg": str(e)})
        else:
            return jsonify(user)


class User(Resource):
    def get(self, user_id):
        try:
            user = service.get_user_by_id(user_id)
        except UserInputException as e:
            return jsonify({"msg": str(e)})
        else:
            return jsonify(user)

    def delete(self, user_id):
        try:
            service.delete_by_id(user_id)
        except UserInputException as e:
            return jsonify({"msg": str(e)})
        else:
            return jsonify({"msg": "user is deleted"})

    def put(self, user_id):
        body = request.json
        try:
            user = service.update_by_id(user_id, body)
        except UserInputException as e:
            return jsonify({"msg": str(e)})
        else:
            return jsonify(user)


api.add_resource(Users, "/")
api.add_resource(User, "/<int:user_id>")
