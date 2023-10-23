from app import app
from app.services.auth_service import AuthService
from flask import render_template, request, redirect, url_for
import platform
import datetime

SKILLS = ["C++", "Python", "Java", "Spring", "Math", "SQL", "REST API", "Git", "Linux", "HTML/CSS"]
AUTH_SERVICE = AuthService()

pre_authorized = AUTH_SERVICE.get_pre_login_decorator()

@app.route("/")
@pre_authorized
def main_page():
    return render_template("index.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/hobbies")
@pre_authorized
def hobbies_page():
    return render_template("hobbies.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/study")
@pre_authorized
def study_page():
    return render_template("studying.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/skills")
@app.route("/skills/<int:id>")
@pre_authorized
def skills_page(id=None):
    is_list = True
    if id:
        skills = SKILLS[id:id + 1] if 0 <= id < len(SKILLS) else ["Wrong index!!!"]
        is_list = False
    else:
        skills = SKILLS

    return render_template("skills.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now(),
                           len=len(skills),
                           is_list=is_list,
                           skills=skills)


@app.route("/login", methods=['GET'])
def login_page():
    return render_template("login.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/login", methods=['POST'])
def login():
    login_input = request.form.get('login')
    password_input = request.form.get('password')
    if AUTH_SERVICE.authenticate(login_input, password_input):
        AUTH_SERVICE.set_session_value(value=login_input)
        return redirect(url_for("main_page"))
    else:
        return render_template("login.html", message="Wrong login or password")
