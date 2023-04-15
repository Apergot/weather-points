from flask import Flask, jsonify
from src.database import Session

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify(hello="world")
