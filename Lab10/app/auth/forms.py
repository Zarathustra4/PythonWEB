from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, AnyOf, Email, Regexp, EqualTo


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


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=14),
                                       Regexp('^[A-Za-z][A-Za-z0-9_\\.]*$', 0,
                                              "Username must only have letters, numbers, dots or " +
                                              "underscores")])

    email = StringField('Email', validators=[DataRequired("Email field mustn't be empty"),
                                             Email()])

    password = PasswordField('Password',
                             validators=[DataRequired("Password field mustn't be empty"),
                                         Length(min=8, max=30),
                                         EqualTo("repeat_password", "Passwords don't match")])

    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(),
                                                                   Length(min=8, max=30)])

    about = TextAreaField("About me", validators=[])
    # TODO: add extensions validator 

    image = FileField("Image", validators=[FileRequired()])
    submit = SubmitField('Sign up')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=14),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_\\.]*$', 0,
                                                          "Username must only have letters, numbers, dots or " +
                                                          "underscores")])
    email = StringField('Email',
                        validators=[DataRequired("Email field mustn't be empty"), Email("It should be an email")])

    about = TextAreaField("About me")

    image = FileField("Image")

    submit = SubmitField('Update')
