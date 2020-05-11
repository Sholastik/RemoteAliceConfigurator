from flask import Flask
from flask_restful import Api

from runner.data import db_session
from runner.data.command_resource import CommandResource, CommandListResource, CommandResourceMany
from runner.data.machine_resource import MachineResource, MachineListResource
from runner.settings import DB_PATH

app = Flask(__name__)
api = Api(app)
api.add_resource(CommandResource, '/command/<int:command_id>')
api.add_resource(CommandResourceMany, '/commands/<int:port>')
api.add_resource(CommandListResource, '/commands')
api.add_resource(MachineResource, '/machine/<int:port>')
api.add_resource(MachineListResource, '/machines')

db_session.global_init(DB_PATH)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
