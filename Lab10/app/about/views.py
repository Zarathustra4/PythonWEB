from flask import Blueprint, render_template

about_bp = Blueprint("about_bp", __name__,
                     template_folder="templates",
                     static_folder="static",
                     url_prefix="/about")

SKILLS = ["C++", "Python", "Java", "Spring", "Math", "SQL", "REST API", "Git", "Linux", "HTML/CSS"]


@about_bp.route("/")
def about_page():
    return render_template("about.html")


@about_bp.route("/study")
def study_page():
    return render_template("studying.html")


@about_bp.route("/skills")
@about_bp.route("/skills/<int:id>")
def skills_page(id=None):
    is_list = True
    if id:
        skills = SKILLS[id:id + 1] if 0 <= id < len(SKILLS) else ["Wrong index!!!"]
        is_list = False
    else:
        skills = SKILLS

    return render_template("skills.html",
                           len=len(skills),
                           is_list=is_list,
                           skills=skills)
