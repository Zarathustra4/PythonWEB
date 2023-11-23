from flask import Blueprint

about_bp = Blueprint("about_bp", __name__,
                     template_folder="templates", url_prefix="/about")
