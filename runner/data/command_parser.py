from flask_restful import reqparse

command_parser = reqparse.RequestParser()
command_parser.add_argument('action_name', required=True)
command_parser.add_argument('trigger', required=True)
command_parser.add_argument('answer', required=True)
command_parser.add_argument('port', required=True)

command_parser_not_required = reqparse.RequestParser()
command_parser_not_required.add_argument('action_name')
command_parser_not_required.add_argument('trigger')
command_parser_not_required.add_argument('answer')
