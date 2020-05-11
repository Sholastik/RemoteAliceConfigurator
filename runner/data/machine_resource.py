from flask import jsonify
from flask_restful import abort, Resource

from runner.data import db_session
from runner.data.machine import Machine
from runner.data.machine_parser import machine_parser

running_machines = {}


def abort_if_not_found(machine_id):
    session = db_session.create_session()
    command = session.query(Machine).get(machine_id)
    if not command:
        abort(404, message=f"Machine {machine_id} not found")


class MachineResource(Resource):
    def delete(self, port):
        abort_if_not_found(port)
        session = db_session.create_session()
        machine = session.query(Machine).get(port)
        session.delete(machine)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self, port):
        abort_if_not_found(port)
        return jsonify({"running": port in running_machines and running_machines[port].is_running()})

    def post(self, port):
        session = db_session.create_session()
        if port in running_machines:
            running_machines[port].stop()
        machine = session.query(Machine).get(port)
        machine.start()
        running_machines[port] = machine
        return {"success": "OK"}


class MachineListResource(Resource):
    def post(self):
        args = machine_parser.parse_args()
        session = db_session.create_session()
        if session.query(Machine).get(args['port']):
            return abort(400, message=f'Machine with {args["port"]} exists!')
        machine = Machine(
            port=args['port']
        )
        session.add(machine)
        session.commit()
        return jsonify({'success': 'OK'})
