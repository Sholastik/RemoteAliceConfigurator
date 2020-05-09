from flask import Flask
from flask_restful import Api

from runner.data import db_session
from runner.data.command_resource import CommandResource, CommandListResource
from runner.settings import DB_PATH

app = Flask(__name__)
api = Api(app)
api.add_resource(CommandResource, '/command')
api.add_resource(CommandListResource, '/commands')

db_session.global_init(DB_PATH)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)
