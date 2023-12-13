import os

from werkzeug.utils import secure_filename

from app.posts.forms import CreatePostForm, UpdatePostForm, TagForm, CatForm
from app.posts.models import PostModel, CategoryModel, TagModel
from datetime import datetime
from flask_login import current_user

import config
from .dto import PostDto
from ..exceptions import UserInputException
from ..extensions import db

NOT_FOUND_MESSAGE = "There is no such a post with id {id}"


def post_model_to_dto(model: PostModel):
    category = CategoryModel.query.filter_by(id=model.category_id).first()
    tags = map(lambda tag: str(tag), model.tags)
    return PostDto(title=model.title,
                   text=model.text,
                   image=model.image,
                   created=model.created,
                   enabled=model.enabled,
                   user_id=model.user_id,
                   category=category.name,
                   id=model.id,
                   post_type=model.post_type,
                   tags=list(tags))


def get_all_cats():
    return CategoryModel.query.all()


def get_all_tags():
    return TagModel.query.all()


def get_create_post_form():
    form = CreatePostForm()
    form.category.choices = [(cat.id, cat.name) for cat in get_all_cats()]
    form.tags.choices = [(tag.id, tag.name) for tag in get_all_tags()]
    return form


def get_all_posts() -> list:
    posts = PostModel.query.all()
    posts_dtos = map(post_model_to_dto, posts)
    posts_dtos = list(posts_dtos)
    posts_dtos.sort(key=lambda dto: dto.created, reverse=True)
    return posts_dtos


def get_post_by_id(id: int) -> PostDto:
    return post_model_to_dto(
        PostModel.query.filter_by(id=id).first()
    )


def delete_post_by_id(id: int) -> None:
    post = PostModel.query.filter_by(id=id).first()
    if post is None:
        raise UserInputException(NOT_FOUND_MESSAGE.format(id=id))

    PostModel.query.filter_by(id=id).delete()
    db.session.commit()


def post_model_to_form(post: PostModel):
    form = UpdatePostForm(title=post.title,
                          text=post.text,
                          image=post.image,
                          post_type=post.post_type)
    form.category.choices = [(cat.id, cat.name) for cat in get_all_cats()]
    form.tags.choices = [(tag.id, tag.name) for tag in get_all_tags()]
    return form


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
    post.created = datetime.now()
    post.image = filename
    post.category_id = post_form.category.data
    post.post_type = post_form.post_type.data
    post.tags = [TagModel.query.get(tag_id) for tag_id in post_form.tags.data]

    db.session.commit()


def create_post(post_form: CreatePostForm):
    date = datetime.now()
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
                     category_id=post_form.category.data,
                     user_id=user_id,
                     tags=[TagModel.query.get(tag_id) for tag_id in post_form.tags.data])

    db.session.add(post)
    db.session.commit()


def create_tag(tag_form: TagForm):
    tag_name = tag_form.tag_name.data
    if TagModel.query.filter_by(name=tag_name).first() is not None:
        raise UserInputException("Such tag already exists")

    tag = TagModel(name=tag_name)
    db.session.add(tag)
    db.session.commit()


def create_cat(cat_form: CatForm):
    cat_name = cat_form.cat_name.data
    if CategoryModel.query.filter_by(name=cat_name).first() is not None:
        raise UserInputException("Such category already exists")

    cat = CategoryModel(name=cat_name)
    db.session.add(cat)
    db.session.commit()
