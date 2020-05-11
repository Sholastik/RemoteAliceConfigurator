from flask import jsonify
from flask_restful import Resource, abort

from runner.data import db_session
from runner.data.command import Command
from runner.data.command_parser import command_parser, command_parser_not_required


def abort_if_not_found(command_id):
    session = db_session.create_session()
    command = session.query(Command).get(command_id)
    if not command:
        abort(404, message=f"Command {command_id} not found")


class CommandResource(Resource):
    def get(self, command_id):
        abort_if_not_found(command_id)
        session = db_session.create_session()
        command = session.query(Command).get(command_id)
        return jsonify({'command': command.to_dict()})

    def delete(self, command_id):
        abort_if_not_found(command_id)
        session = db_session.create_session()
        command = session.query(Command).get(command_id)
        session.delete(command)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, command_id):
        abort_if_not_found(command_id)
        args = command_parser_not_required.parse_args()
        session = db_session.create_session()
        command = session.query(Command).get(command_id)
        for token in ('action_name', 'trigger', 'answer'):
            if token in args and args[token] is not None:
                exec(f"command.{token} = '{args[token]}'")
        session.commit()
        return jsonify({'success': 'OK'})


class CommandResourceMany(Resource):
    def get(self, port):
        session = db_session.create_session()
        commands = session.query(Command).filter(Command.port == port).all()
        return jsonify({"commands": [x.to_dict() for x in commands]})


class CommandListResource(Resource):
    def post(self):
        args = command_parser.parse_args()
        session = db_session.create_session()
        command = Command(
            action_name=args['action_name'],
            trigger=args['trigger'],
            answer=args['answer'],
            port=args['port']
        )
        session.add(command)
        session.commit()
        return jsonify({'success': 'OK'})
