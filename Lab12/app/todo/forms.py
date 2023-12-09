from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.todo.models import StatusEnum


class TodoForm(FlaskForm):
    todo = StringField('To Do', validators=[DataRequired()])
    status = SelectField('Status', choices=[(e.name, e.value) for e in StatusEnum])
    submit = SubmitField('Add task')
