from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo


class SignUpForm(FlaskForm):
    skill_name = StringField('Название навыка', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[
        DataRequired(), EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
