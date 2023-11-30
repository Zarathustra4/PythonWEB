from flask import Blueprint
from flask import render_template

posts_bp = Blueprint("post_bp", __name__, 
                     template_folder="templates", url_prefix="/posts")

@posts_bp.route("/create", methods=["GET"])
def create_post_page():
    return render_template("create_post.html")
