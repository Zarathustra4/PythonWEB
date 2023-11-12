from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, AnyOf, Email, Regexp
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


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=14),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_\\.]*$', 0,
                                                          "Username must only have letters, numbers, dots or " +
                                                          "underscores")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Sign up')
