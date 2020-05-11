from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ActionEditForm(FlaskForm):
    action_name = StringField('Название действия', validators=[DataRequired()])
    trigger = StringField('Активационная фраза', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Обновить')
