import flask
from flask import render_template
from flask_login import login_required, current_user

from configurator.forms.action import ActionForm

console_blueprint = flask.Blueprint('console', __name__, template_folder='templates')


@console_blueprint.route('/console')
@login_required
def console():
    return render_template("console_main.html", skill=current_user)


@console_blueprint.route('/console/add', methods=["GET", "POST"])
@login_required
def add():
    form = ActionForm()

    if form.validate_on_submit():
        pass
    
    return render_template("console_add.html", skill=current_user, form=form)
