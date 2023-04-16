import os
from flask import Flask, request, abort, jsonify
from ..database.models import setup_db


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"