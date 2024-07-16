from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    patrol_id = StringField('Nazwa Patrolu', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

class TaskForm(FlaskForm):
    keyword = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Wyślij')
