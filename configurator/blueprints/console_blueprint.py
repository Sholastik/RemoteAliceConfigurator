import flask
from flask import render_template, redirect
from flask_login import current_user
from requests import get, post, delete, put

from configurator.forms.action_add import ActionAddForm
from configurator.forms.action_edit import ActionEditForm
from configurator.util.auth import login_required

console_blueprint = flask.Blueprint('console', __name__, template_folder='templates')


@login_required
@console_blueprint.route('/console')
def console():
    commands = get(f"http://127.0.0.1:8081/commands/{current_user.port}").json()["commands"]
    running = get(f"http://127.0.0.1:8081/machine/{current_user.port}").json()['running']
    print(running)

    return render_template("console_main.html", skill=current_user, commands=commands, running=running)


@login_required
@console_blueprint.route('/console/add', methods=["GET", "POST"])
def add():
    form = ActionAddForm()

    if form.validate_on_submit():
        name = form.action_name.data
        trigger = form.trigger.data
        answer = form.answer.data
        post(f"http://127.0.0.1:8081/commands",
             json={
                 "action_name": name,
                 "trigger": trigger,
                 "answer": answer,
                 "port": current_user.port
             })
        return redirect("/console")

    running = get(f"http://127.0.0.1:8081/machine/{current_user.port}").json()['running']
    print(running)

    return render_template("console_add.html", skill=current_user, form=form, running=running)


@console_blueprint.route('/console/edit/<int:command_id>/', methods=["GET", "POST"])
@login_required
def edit(command_id):
    form = ActionEditForm()

    if form.validate_on_submit():
        name = form.action_name.data
        trigger = form.trigger.data
        answer = form.answer.data
        put(f"http://127.0.0.1:8081/command/{command_id}",
            json={
                "action_name": name,
                "trigger": trigger,
                "answer": answer,
                "port": current_user.port
            })
        return redirect("/console")

    command = get(f"http://127.0.0.1:8081/command/{command_id}").json()["command"]
    form.action_name.data = command["action_name"]
    form.trigger.data = command["trigger"]
    form.answer.data = command["answer"]

    running = get(f"http://127.0.0.1:8081/machine/{current_user.port}").json()['running']
    print(running)

    return render_template("console_edit.html", action=command, form=form, running=running)


@login_required
@console_blueprint.route('/console/remove/<int:command_id>')
def remove(command_id):
    delete(f"http://127.0.0.1:8081/command/{command_id}")
    return redirect("/console")


@login_required
@console_blueprint.route('/console/restart')
def restart():
    post(f"http://127.0.0.1:8081/machine/{current_user.port}")
    return redirect("/console")
