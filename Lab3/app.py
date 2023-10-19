from flask import Flask, render_template, request
import platform

app = Flask(__name__)


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


