from flask import Flask, render_template, request
import platform

app = Flask(__name__)

SKILLS = ["C++", "Python", "Java", "Spring", "Math", "SQL", "REST API", "Git", "Linux", "HTML/CSS"]

@app.route("/")
def main_page():
    return render_template("index.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent)


@app.route("/hobbies")
def hobbies_page():
    return render_template("hobbies.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent)


@app.route("/study")
def study_page():
    return render_template("studying.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent)


@app.route("/skills")
@app.route("/skills/<int:id>")
def skills_page(id=None):
    if id:
        try:
            skills = SKILLS[id:id + 1]
        except IndexError:
            skills = ["Wrong index!!!"]
    else:
        skills = SKILLS

    return render_template("skills.html",
                           os_name=platform.system(),
                           user_agent=request.user_agent,
                           len=len(skills),
                           skills=skills)
