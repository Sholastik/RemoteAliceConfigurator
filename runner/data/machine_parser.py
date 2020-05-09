from flask_restful.reqparse import RequestParser

machine_parser = RequestParser()
machine_parser.add_argument('port', required=True)
