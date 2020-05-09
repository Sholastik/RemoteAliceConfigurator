import flask
from flask import redirect, render_template
from flask_login import current_user, login_user, logout_user

from configurator.data import db_session
from configurator.data.skill import Skill
from configurator.forms.login import LoginForm
from configurator.forms.signup import SignUpForm
from configurator.util import auth
from configurator.util.auth import check_password

auth_blueprint = flask.Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Проверяем, зашел ли пользователь в аккаунт
    if current_user.is_authenticated:
        return redirect('/console')

    form = LoginForm()

    # Валидация формы
    if form.validate_on_submit():
        session = db_session.create_session()

        # Получаем хеш пароля аккаунта с данным именем
        skill = session.query(Skill).filter(Skill.skill_name == form.skill_name.data).first()

        # Проверяем, существует ли такой аккаунт и верно ли введен пароль
        if skill:
            salt, hashed_password = skill.salt, skill.hashed_password

            if check_password(salt, hashed_password, form.password.data):
                login_user(skill, remember=form.remember_me.data)
                return redirect("/console")

        return render_template('login.html', message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # Проверяем, зашел ли пользователь в аккаунт
    if current_user.is_authenticated:
        # Возвращаем на страницу входа
        return redirect('/login')

    form = SignUpForm()

    # Валидация формы
    if form.validate_on_submit():
        session = db_session.create_session()

        # Проверяем, существует ли аккаунт с таким именем
        if session.query(Skill).filter(Skill.skill_name == form.skill_name.data).first() is not None:
            return render_template('signup.html', title='Регистрация', form=form,
                                   message="Навык с таким названием уже существует.")

        # Создаем навык
        salt, password = auth.prepare_password(form.password.data)
        skill = Skill(skill_name=form.skill_name.data, hashed_password=password,
                      salt=salt, port=5000 + session.query(Skill).count()
                      )

        session.add(skill)
        session.commit()

        # Выполняем вход в аккаунт
        login_user(skill)
        return redirect('/login')

    return render_template('signup.html', title='Регистрация', form=form)


@auth_blueprint.route('/sign_out')
def sign_out():
    logout_user()
    return redirect('/')
