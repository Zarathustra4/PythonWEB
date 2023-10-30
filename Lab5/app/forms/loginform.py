from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


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