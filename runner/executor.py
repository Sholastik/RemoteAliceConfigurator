import json
import logging
from argparse import ArgumentParser

from flask import Flask, request
from requests import get

parser = ArgumentParser()
parser.add_argument("port", type=int)
port = parser.parse_args().port

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}

commands = get(f"http://127.0.0.1:8081/commands/{port}").json()['commands']
commands = {x['trigger'].lower(): x['answer'] for x in commands}


@app.route('/check')
def ping():
    return f"I'm running at localhost:{port}!"


@app.route('/alice', methods=["POST"])
def alice():
    logging.info(f"Request: {request.json}")

    response = {
        "session": request.json["session"],
        "version": request.json["version"],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f"Response: {response!r}")

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req["session"]["user_id"]

    if req["session"]["new"]:
        res["response"]["text"] = commands["приветствие"]
        return

    if req["request"]["original_utterance"].lower() in commands:
        res["response"]["text"] = commands[req["request"]["original_utterance"].lower()]
        return

    res["response"]["text"] = "Такой команды нет!"


if __name__ == '__main__':
    app.run(port=port)
