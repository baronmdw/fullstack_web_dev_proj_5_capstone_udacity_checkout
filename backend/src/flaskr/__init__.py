import os
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"