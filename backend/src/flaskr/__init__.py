import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from .database.models import setup_db, Connectiontest, Receipes, Ingredient, ingredientsPerReceipe, db
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
        newReceipe = Receipes(name="Test",description="Gotta find out")
        newReceipe.insert()
        newIngredient = Ingredient(name="Nudel", unit="gram")
        newIngredient.insert()
        print(newReceipe.id)
        ingredient = ingredientsPerReceipe(ingredient_id=newIngredient.id, receipe_id=newReceipe.id, amount=300)
        ingredient.insert()
        return (connections_formatted)
    
    @app.route("/receipes", methods=["GET"])
    @cross_origin()
    def get_receipes():
        receipes = Receipes.query.all()
        receipes_formatted = [r.format() for r in receipes]
        responseObject = {
            "success": True,
            "receipes": receipes_formatted
        }
        return jsonify(responseObject)

    @app.route("/receipes", methods=["POST"])
    @cross_origin()
    def post_receipe():
        inputReceipe = request.get_json()
        try:
            newReceipe = Receipes(name=inputReceipe["name"], description=inputReceipe["receipe"])
            newReceipe.insert()
            return jsonify({"success": True})
        except:
            db.session.rollback()
            abort(400)
    
    return app