from flask import Flask
from handle_core import get_directurl
from data_access import save, read
import json
from setting import BANNER,VERSION

# config
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def display():
    records = read()
    return "内容：<h3>" + json.dumps(records) + "</h3>"


def start_web():
    app.run(host='127.0.0.1', port=8080, debug=True)
