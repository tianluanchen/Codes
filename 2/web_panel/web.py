from flask import Flask
from api.data_access import read
import json

# config
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def display():
    records = read()
    return "内容：<h3>" + json.dumps(records) + "</h3>"


def start_web():
    app.run(host='127.0.0.1', port=8080, debug=True)
