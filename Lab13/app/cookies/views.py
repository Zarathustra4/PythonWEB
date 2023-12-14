import datetime
import platform

from flask import Blueprint, redirect, url_for, render_template
from flask import request, session
from flask_login import login_required, current_user

cookies_bp = Blueprint("cookies_bp", __name__,
                       template_folder="templates", url_prefix="/cookies")


@cookies_bp.route("/", methods=["GET"])
def cookies_page():
    return render_template("cookies.html",
                           cookies=dict(session),
                           user_login=current_user.username,
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now()
                           )


@cookies_bp.route("/", methods=["POST"])
@login_required
def post_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    session[key] = value
    return redirect(url_for("cookies_bp.cookies_page"))


@cookies_bp.route("/delete/<key>", methods=["POST"])
@cookies_bp.route("/delete", methods=["POST"])
def delete_cookie(key=None):
    if key:
        session.pop(key)
    else:
        session.clear()
    return redirect(url_for("cookies_bp.cookies_page"))
