from flask import Blueprint, flash
from flask import render_template, redirect, url_for
from flask_login import login_required

from app.exceptions import UserInputException
from app.posts import service
from app.posts.forms import CreatePostForm

posts_bp = Blueprint("posts_bp", __name__,
                     template_folder="templates",
                     url_prefix="/posts")


# TODO: add restricted photo size and shape

@posts_bp.route("/")
@login_required
def main_page():
    posts = service.get_all_posts()
    return render_template("main.html", posts=posts)


@posts_bp.route("/<int:id>")
def post_page(id: int):
    if id is None:
        flash("There is no post with such id")
    post = service.get_post_by_id(id)
    return render_template("post.html", post=post)


@posts_bp.route("/create", methods=["GET"])
@login_required
def create_post_page():
    form = service.get_create_post_form()
    return render_template("create_post.html", form=form)


@posts_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    form = CreatePostForm()
    service.create_post(form)
    return redirect(url_for("posts_bp.main_page"))


@posts_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_post(id: int):
    try:
        service.delete_post_by_id(id)
    except UserInputException as e:
        flash(str(e), category="error")
    else:
        flash("The post was deleted")
    return redirect(url_for("posts_bp.main_page"))


@posts_bp.route("/<int:id>/update", methods=["GET"])
@login_required
def update_page(id: int):
    post_form = service.get_post_form_by_id(id)
    return render_template("update_post.html", form=post_form, id=id)


@posts_bp.route("/<int:id>/update", methods=["POST"])
@login_required
def update(id: int):
    post_form = CreatePostForm()
    service.update_post(id, post_form)
    return redirect(url_for("posts_bp.main_page"))
