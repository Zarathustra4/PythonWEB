import os

from werkzeug.utils import secure_filename

from app.posts.forms import CreatePostForm, UpdatePostForm
from app.posts.models import PostModel
from datetime import datetime
from flask_login import current_user

import config
from ..exceptions import UserInputException
from ..extensions import db

NOT_FOUND_MESSAGE = "There is no such a post with id {id}"


def get_all_posts() -> list:
    return PostModel.query.all()


def get_post_by_id(id: int) -> PostModel:
    return PostModel.query.filter_by(id=id).first()


def delete_post_by_id(id: int) -> None:
    post = PostModel.query.filter_by(id=id).first()
    if post is None:
        raise UserInputException(NOT_FOUND_MESSAGE.format(id=id))

    PostModel.query.filter_by(id=id).delete()
    db.session.commit()


def post_model_to_form(post: PostModel):
    return UpdatePostForm(title=post.title,
                          text=post.text,
                          image=post.image,
                          post_type=post.post_type)


def get_post_form_by_id(id: int):
    post = PostModel.query.filter_by(id=id).first()
    if post is None:
        raise UserInputException(NOT_FOUND_MESSAGE.format(id=id))

    return post_model_to_form(post)


def update_post(id: int, post_form: CreatePostForm):
    post = PostModel.query.filter_by(id=id).first()

    if post is None:
        raise UserInputException(NOT_FOUND_MESSAGE.format(id=id))

    image = post_form.image.data
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(
            config.basedir, 'app', 'static', 'images', filename
        ))
    else:
        filename = post.image

    post.title = post_form.title.data
    post.text = post_form.text.data
    post.created = datetime.now().date()
    post.image = filename

    db.session.commit()


def create_post(post_form: CreatePostForm):
    date = datetime.now().date()
    user_id = current_user.get_id()

    image = post_form.image.data

    filename = secure_filename(image.filename)
    image.save(os.path.join(
        config.basedir, 'app', 'static', 'posts', 'images', filename
    ))

    post = PostModel(title=post_form.title.data,
                     text=post_form.text.data,
                     image=filename,
                     created=date,
                     post_type=post_form.post_type.data,
                     user_id=user_id)

    db.session.add(post)
    db.session.commit()
