from argparse import ArgumentParser

from flask import Flask

parser = ArgumentParser()
parser.add_argument("port", type=int)
port = parser.parse_args().port

app = Flask(__name__)


@app.route('/check')
def ping():
    return f"I'm running at localhost:{port}!"


if __name__ == '__main__':
    app.run(port=port)
