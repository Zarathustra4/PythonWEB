from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required

from app.posts import service
from app.posts.forms import CreatePostForm

posts_bp = Blueprint("posts_bp", __name__,
                     template_folder="templates", url_prefix="/posts")


@posts_bp.route("/")
@login_required
def main_page():
    return "main.html"


@posts_bp.route("/create", methods=["GET"])
@login_required
def create_post_page():
    form = CreatePostForm()
    return render_template("create_post.html", form=form)


@posts_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    form = CreatePostForm()
    service.create_post(form)
    return redirect(url_for("posts_bp.main_page"))
