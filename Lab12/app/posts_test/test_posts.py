from io import BytesIO

import pytest

from app import create_app
from ..auth.models import UserModel
from ..posts.models import PostModel

TEST_USERNAME = "test_user"
TEST_EMAIL = "test_user@gmail.com"
TEST_PASSWORD = "11111111"


@pytest.fixture
def app():
    """Fixture for app"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    return app


@pytest.fixture
def login(client, app, database):
    """Fixture for login test user"""
    with app.app_context():
        data = {'username': TEST_USERNAME,
                'email': TEST_EMAIL}

        test_user = UserModel(**data)
        test_user.set_password(TEST_PASSWORD)

        if UserModel.query.filter_by(username=TEST_USERNAME).first() is None:
            database.session.add(test_user)

        client.post("/login",
                    data=dict(
                        login=TEST_USERNAME,
                        password=TEST_PASSWORD,
                        remember='y',
                        submit='Log In'
                    ))

        return test_user


@pytest.fixture
def client(app):
    """Fixture for app client"""
    return app.test_client()


@pytest.fixture
def database(app):
    """Fixture for database"""
    with app.app_context():
        from ..extensions import db

        db.create_all()
        yield db
        # db.drop_all()


def test_main_page(client, app, login):
    """Test for posts page"""
    with app.app_context():
        response = client.get("/posts")
        assert response.status == '200 OK'
        assert b"Create post" in response.data


def test_create_post(client, app, login):
    """Test for creating post"""
    with app.app_context():
        response = client.post(
            "/posts/create",
            data=dict(
                title="Test Post",
                text="Test post",
                type="Publication",
                image=(BytesIO(b'file content'), 'default.jpg')
            )
        )
        assert response.status == "302 FOUND"
        assert PostModel.query.filter_by(title="Test Post").first() is not None
        assert PostModel.query.filter_by(text="Test post").first().title == "Test Post"


