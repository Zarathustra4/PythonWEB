from app import app
from app import auth
from flask import render_template, request
import platform
import datetime

SKILLS = ["C++", "Python", "Java", "Spring", "Math", "SQL", "REST API", "Git", "Linux", "HTML/CSS"]


@app.route("/")
def main_page():
    return render_template("index.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/hobbies")
def hobbies_page():
    return render_template("hobbies.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/study")
def study_page():
    return render_template("studying.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           time=datetime.datetime.now())


@app.route("/skills")
@app.route("/skills/<int:id>")
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
    if auth.authenticate(login_input, password_input):
        return render_template("index.html", os_name=platform.system(),
                               user_agent=request.user_agent,
                               time=datetime.datetime.now())
    else:
        return render_template("error.html", message="Wrong login or password")
