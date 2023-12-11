import unittest

from flask import url_for
from flask_login import login_user
from flask_testing import TestCase

from app import create_app
from app.auth.models import UserModel
from app.todo.models import TodoModel, StatusEnum
from ..extensions import db

TEST_USERNAME = "test_user"
TEST_EMAIL = "test_user@gmail.com"
TEST_PASSWORD = "11111111"


def login():
    test_user = UserModel(username=TEST_USERNAME, email=TEST_EMAIL)
    password = TEST_PASSWORD
    test_user.set_password(password)

    login_user(test_user, remember=True)


class AuthTest(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app

    def setUp(self):
        db.create_all()
        login()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_creation(self):
        """Test of todo creation"""

        response = self.client.post(
            url_for("todo_bp.create_todo"),
            data=dict(
                todo="Test Todo",
                status="TODO",
                submit="Add task"
            )
        )
        expected_location = url_for("todo_bp.todo_page")
        self.assertEqual(expected_location, response.location)
        created_todo = TodoModel.query.filter_by(todo="Test Todo").first()
        self.assertIsNotNone(created_todo)

    def test_update(self):
        """Test updating todo"""

        test_todo = TodoModel(todo="Update test", status="TODO")
        db.session.add(test_todo)

        id = TodoModel.query.filter_by(todo="Update test").first().id
        response = self.client.post(
            url_for("todo_bp.todo_update", id=str(id)),
            data=dict(
                todo="Update test completed",
                status="DONE"
            )
        )

        expected_location = url_for("todo_bp.todo_page")
        self.assertEqual(expected_location, response.location)

        update_todo = TodoModel.query.filter_by(id=id).first()
        self.assertEqual(update_todo.todo, "Update test completed")
        self.assertEqual(update_todo.status, StatusEnum.DONE)

    def test_delete(self):
        """Test deleting todo"""

        test_todo = TodoModel(todo="Delete test", status="TODO")
        db.session.add(test_todo)

        id = TodoModel.query.filter_by(todo="Delete test").first().id

        response = self.client.post(
            url_for('todo_bp.todo_delete', id=str(id))
        )

        expected_location = url_for("todo_bp.todo_page")
        self.assertEqual(expected_location, response.location)

        deleted_todo = TodoModel.query.filter_by(id=id).first()
        self.assertIsNone(deleted_todo)


if __name__ == '__main__':
    unittest.main()
