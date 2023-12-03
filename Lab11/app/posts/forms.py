from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, TextAreaField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.posts.models import TypeEnum


class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text")
    image = FileField("Image", validators=[FileRequired()])
    post_type = SelectField("Type", choices=[(e.name, e.value) for e in TypeEnum])
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Create a post')


class UpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text")
    image = FileField("Image")
    post_type = SelectField("Type", choices=[(e.name, e.value) for e in TypeEnum])
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Update a post')
