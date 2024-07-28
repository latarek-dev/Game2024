from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    patrol_id = StringField('Nazwa Patrolu', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

class TaskForm(FlaskForm):
    keyword = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Wyślij')

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('Nowe Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź Hasło', validators=[
        DataRequired(), EqualTo('new_password', message='Hasła muszą się zgadzać')])
    submit = SubmitField('Zmień Hasło')