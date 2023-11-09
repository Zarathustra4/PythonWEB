from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, AnyOf
from app.domain.models import StatusEnum


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember', default=False)
    submit = SubmitField("Log In")


class ChangePassForm(FlaskForm):
    old_password = StringField('Old Password', validators=[DataRequired(), Length(min=4, max=10)])
    new_password = StringField('New Password', validators=[DataRequired(), Length(min=4, max=10)])
    repeated_password = StringField('Repeat Password', validators=[DataRequired(), Length(min=4, max=10)])
    submit = SubmitField("Change Password")


class FeedbackForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired()])
    message = TextAreaField('Відгук', validators=[DataRequired()])
    submit = SubmitField('Надіслати')


class TodoForm(FlaskForm):
    todo = StringField('To Do', validators=[DataRequired()])
    status = SelectField('Status', choices=[(e.name, e.value) for e in StatusEnum])
    submit = SubmitField('Add task')
