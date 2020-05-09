from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    skill_name = StringField('Название навыка', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
