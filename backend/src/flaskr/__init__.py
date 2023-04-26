import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from .database.models import setup_db, Connectiontest, db
from flask_migrate import Migrate

def create_app(dbURI='', test_config=None):
    if dbURI == "":
        DB_HOST = os.environ.get("DB_HOST")
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_NAME = os.environ.get("DB_NAME")
        DB_PORT = os.environ.get("DB_PORT")
        dbURI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
        
    app = Flask(__name__)
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=dbURI)
    setup_db(app, dbURI)
    Migrate(app,db)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route("/")
    @cross_origin()
    def index():
        connections = Connectiontest.query.all()
        connections_formatted = [c.format() for c in connections]
        print(connections_formatted)
        return (connections_formatted)
    
    return app