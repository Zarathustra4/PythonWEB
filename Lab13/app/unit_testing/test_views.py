import unittest
from flask import url_for
from flask_login import login_user
from flask_testing import TestCase

from app import create_app
from app.auth.views import logout
from app.auth.models import UserModel

TEST_USERNAME = "test_user"
TEST_EMAIL = "test_user@gmail.com"
TEST_PASSWORD = "11111111"

TEST_REGISTER_USERNAME = "register"
TEST_REGISTER_EMAIL = "register@gmail.com"
TEST_REGISTER_PASSWORD = "11111111"


def login():
    test_user = UserModel(username=TEST_USERNAME, email=TEST_EMAIL)
    password = TEST_PASSWORD
    test_user.set_password(password)

    login_user(test_user, remember=True)


class ViewsTest(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        return app

    def test_homepage(self):
        """Test of home page response"""
        login()

        response = self.client.get(url_for('auth_bp.main_page'))
        self.assert200(response)
        self.assertIn(b'test_user', response.data)

    def test_todo_page(self):
        """Test of todo page response"""
        login()

        response = self.client.get(url_for('todo_bp.todo_page'))
        self.assert200(response)
        self.assertIn(b'Todo', response.data)

    def test_posts_page(self):
        """Test of posts page response"""
        login()

        response = self.client.get(url_for("posts_bp.main_page"))
        self.assert200(response)
        self.assertIn(b'Create post', response.data)


if __name__ == '__main__':
    unittest.main()
