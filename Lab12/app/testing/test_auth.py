import unittest
from io import BytesIO

from flask import url_for
from flask_testing import TestCase

from app import create_app
from app.auth.views import logout
from app.auth.models import UserModel
from ..extensions import db

TEST_USERNAME = "test_user"
TEST_EMAIL = "test_user@gmail.com"
TEST_PASSWORD = "11111111"

TEST_REGISTER_USERNAME = "register"
TEST_REGISTER_EMAIL = "register@gmail.com"
TEST_REGISTER_PASSWORD = "11111111"


class AuthTest(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app

    def setUp(self):
        logout()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_success_register(self):
        """Test of registration"""
        data = {'username': TEST_REGISTER_USERNAME,
                'email': TEST_REGISTER_EMAIL,
                'password': TEST_REGISTER_PASSWORD,
                'repeat_password': TEST_REGISTER_PASSWORD,
                'image': (BytesIO(b'file content'), 'default.jpg')}

        response = self.client.post(url_for('auth_bp.signup'), data=data)
        registered_user = UserModel.query.filter_by(username=TEST_REGISTER_USERNAME).first()
        self.assertIsNotNone(registered_user)

    def test_success_login(self):
        """Test of success login"""
        logout()
        response = self.client.post(url_for('auth_bp.login_page'), data=dict(
            login=TEST_USERNAME,
            password=TEST_PASSWORD,
            remember='y',
            submit='Log In'
        ))

        expected_location = url_for("auth_bp.main_page")
        self.assertEqual(response.location, expected_location)

    def test_failed_login(self):
        """Test of failed login"""
        response = self.client.post(url_for('auth_bp.login_page'),
                                    data=dict(
                                        login=TEST_USERNAME,
                                        password="Wrong password",
                                        remember='y',
                                        submit='Log In'
                                    ))

        expected_location = url_for("auth_bp.login_page")
        self.assertEqual(response.location, expected_location)

    def test_logout(self):
        """Test of logout"""
        # Login
        data = {'username': TEST_USERNAME,
                'email': TEST_EMAIL}

        test_user = UserModel(**data)
        test_user.set_password(TEST_PASSWORD)

        db.session.add(test_user)

        response = self.client.post(url_for('auth_bp.login_page'), data=dict(
            login=TEST_USERNAME,
            password=TEST_PASSWORD,
            remember='y',
            submit='Log In'
        ))

        # Test of login success
        expected_location = url_for("auth_bp.main_page")
        self.assertEqual(response.location, expected_location)

        # Logout
        response = self.client.post(url_for("auth_bp.logout"))
        expected_location = url_for("auth_bp.login_page")
        self.assertEqual(response.location, expected_location)

        # Try to get main page, expected: redirect to login page
        response = self.client.get(url_for("auth_bp.main_page"))
        expected_location = url_for("auth_bp.login_page")
        self.assertTrue(response.location.startswith(expected_location))


if __name__ == '__main__':
    unittest.main()
