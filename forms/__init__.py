from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    patrol_id = StringField('ID Patrolu', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

class TaskForm(FlaskForm):
    keyword = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Wyślij')
