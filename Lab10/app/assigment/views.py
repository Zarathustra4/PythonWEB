from flask import Blueprint

assigment_bp = Blueprint("assigment_bp", __name__,
                     template_folder="templates", url_prefix="/assigment")
