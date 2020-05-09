from flask import Flask, render_template
from flask_login import LoginManager

from configurator.blueprints.auth_blueprint import auth_blueprint
from configurator.data import db_session
from configurator.data.skill import Skill
from configurator.settings import *
from configurator.util.auth import login_required

app = Flask(__name__)
login_manager = LoginManager()

app.secret_key = SECRET_KEY
login_manager.init_app(app)

db_session.global_init(DB_PATH)

app.register_blueprint(auth_blueprint)


@login_manager.user_loader
def load_skill(skill_id):
    # Получение аккаунта, в который ранее входил пользователь
    session = db_session.create_session()
    return session.query(Skill).filter(Skill.id == skill_id).first()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/console')
@login_required
def console():
    return render_template("base.html", title="Console")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
