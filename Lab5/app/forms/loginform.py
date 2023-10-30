from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('remember', default=False)
    submit = SubmitField("Sign In")
