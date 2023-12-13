import io
import pytest
from werkzeug.datastructures import FileStorage

from app import create_app
from ..auth.models import UserModel
from ..extensions import db
from ..posts.models import PostModel, CategoryModel, TagModel, TypeEnum

TEST_USERNAME = "test_user"
TEST_EMAIL = "test_user@gmail.com"
TEST_PASSWORD = "11111111"

TEST_POST_TITLE = "Test post title"
TEST_POST_TEXT = "Test post text"
TEST_POST_TYPE = "PUBLICATION"
IMAGE_PATH = "E:\\Лабораторні\\3 курс\\Python WEB\\Lab12\\app\\posts_test\\unity.jpg"


def create_tag_cat(db):
    cat = CategoryModel(id=1, name="cat")
    tag = TagModel(id=1, name="tag")
    db.session.add(cat)
    db.session.add(tag)


@pytest.fixture
def client():
    """Fixture for app"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            create_tag_cat(db)

            yield client

            db.session.remove()
            db.drop_all()


@pytest.fixture
def login(client):
    """Fixture for login test user"""
    data = {'username': TEST_USERNAME,
            'email': TEST_EMAIL}

    test_user = UserModel(**data)

    test_user.set_password(TEST_PASSWORD)

    if UserModel.query.filter_by(username=TEST_USERNAME).first() is None:
        db.session.add(test_user)

    client.post("/login",
                data=dict(
                    login=TEST_USERNAME,
                    password=TEST_PASSWORD,
                    remember='y'
                ))


@pytest.fixture
def post_id(client, login):
    with open(IMAGE_PATH, "rb") as image_file:
        image = FileStorage(stream=io.BytesIO(image_file.read()), filename='unity.jpg', content_type='image/jpeg')

    client.post(
        "/posts/create",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT,
            type=TEST_POST_TYPE,
            image=(image, "unity.jpg"),
            category=1,
            tags=1
        )
    )

    yield PostModel.query.filter_by(title=TEST_POST_TITLE).first().id


def test_main_page(client, login):
    """Test for posts page"""

    response = client.get("/posts", follow_redirects=True)
    assert response.status_code == 200
    assert b"Create post" in response.data


def test_create_post(client, login):
    """Test for creating post"""
    response = client.post(
        "/posts/create",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT,
            post_type=TEST_POST_TYPE,
            image=(io.BytesIO(b"abcd"), "image.jpg"),
            category=1,
            tags=1
        )
    )
    assert response.status_code == 302
    assert PostModel.query.filter_by(title=TEST_POST_TITLE).first() is not None
    assert PostModel.query.filter_by(text=TEST_POST_TEXT).first().title == TEST_POST_TITLE


def test_update_post(client, login, post_id):
    """Test for updating post"""

    response = client.post(
        f"/posts/{post_id}/update",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT + " New",
            post_type=TEST_POST_TYPE,
            category=1,
            tags=1
        )
    )
    assert response.status_code == 302
    assert PostModel.query.filter_by(title=TEST_POST_TITLE).first().text == TEST_POST_TEXT + " New"


def test_delete_post(client, login, post_id):
    response = client.post(f"/posts/{post_id}/delete")

    assert response.status_code == 302
    assert PostModel.query.filter_by(id=post_id).first() is None


def test_create_tag(client, login):
    res = client.post(
        "/posts/tag",
        data=dict(
            tag_name="test_tag"
        )
    )

    assert res.status_code == 302
    assert TagModel.query.filter_by(name="test_tag").first() is not None


def test_create_cat(client, login):
    res = client.post(
        "/posts/cat",
        data=dict(
            cat_name="test_cat"
        )
    )

    assert res.status_code == 302
    assert CategoryModel.query.filter_by(name="test_cat").first() is not None


def test_post_page(client, login, post_id):
    res = client.get(f"/posts/{post_id}")

    data = res.get_data(as_text=True)

    assert res.status_code == 200
    assert TEST_POST_TITLE in data
    assert TEST_POST_TEXT in data
    assert "#tag" in data
    assert "cat" in data
