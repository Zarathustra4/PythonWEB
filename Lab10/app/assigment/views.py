from flask import Blueprint, render_template, flash, redirect, url_for

from app.assigment.forms import FeedbackForm
from app.assigment.models import ReviewModel
from ..extensions import db

assigment_bp = Blueprint("assigment_bp", __name__,
                         template_folder="templates", url_prefix="/review")


@assigment_bp.route("/", methods=["GET"])
def review_page():
    form = FeedbackForm()
    feedbacks = ReviewModel.query.all()
    return render_template('review.html', form=form, feedbacks=feedbacks)


@assigment_bp.route("/", methods=["POST"])
def review():
    review_form = FeedbackForm()
    if not review_form.validate():
        flash("Review form input is not valid!!!!", category="error")
        return redirect(url_for("assigment_bp.review_page"))

    try:
        name = review_form.name.data
        message = review_form.message.data
        review = ReviewModel(name=name, message=message)
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        flash(str(e), category="error")
    else:
        flash("Your review is added!", category="info")

    return redirect(url_for("assigment_bp.review_page"))
