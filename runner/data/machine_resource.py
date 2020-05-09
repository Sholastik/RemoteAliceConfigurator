from flask import jsonify
from flask_restful import abort, Resource

from runner.data import db_session
from runner.data.machine import Machine
from runner.data.machine_parser import machine_parser


def abort_if_not_found(machine_id):
    session = db_session.create_session()
    command = session.query(Machine).get(machine_id)
    if not command:
        abort(404, message=f"Machine {machine_id} not found")


class MachineResource(Resource):
    def delete(self, machine_id):
        abort_if_not_found(machine_id)
        session = db_session.create_session()
        machine = session.query(Machine).get(machine_id)
        session.delete(machine)
        session.commit()
        return jsonify({'success': 'OK'})


class MachineListResource(Resource):
    def post(self):
        args = machine_parser.parse_args()
        session = db_session.create_session()
        machine = Machine(
            port=args['port']
        )
