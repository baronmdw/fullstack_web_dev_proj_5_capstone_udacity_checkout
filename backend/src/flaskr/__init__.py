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
            for ingredient in inputReceipe["ingredients"]:
                existingIngredient = Ingredient.query.filter(Ingredient.name.ilike(ingredient["name"]), Ingredient.unit.ilike(ingredient["unit"])).one_or_none()
                if existingIngredient:
                    ingredientId = existingIngredient.id
                else:
                    newIngredient = Ingredient(name=ingredient["name"], unit=ingredient["unit"])
                    newIngredient.insert()
                    ingredientId = newIngredient.id
                newIngredientMap = ingredientsPerReceipe(ingredient_id=ingredientId, receipe_id=newReceipe.id, amount=ingredient["amount"])
                newIngredientMap.insert()
            return jsonify({"success": True})
        except:
            db.session.rollback()
            abort(400)
    
    @app.route("/receipes/<int:id>", methods=["GET"])
    @cross_origin()
    def get_receipe(id):
        receipe = Receipes.query.get(id)
        receipeToSend = receipe.format()
        ingredientMap = ingredientsPerReceipe.query.filter_by(receipe_id = id)
        ingredientMapFormatted = [item.format() for item in ingredientMap]
        ingredients = []
        for ingredientMapElement in ingredientMapFormatted:
            ingredientToAdd = Ingredient.query.get(ingredientMapElement["ingredient_id"])
            ingredientOfInterest = ingredientToAdd.format()
            ingredients.append({"id": ingredientOfInterest["id"], "name": ingredientOfInterest["name"], "amount": ingredientMapElement["amount"], "unit": ingredientOfInterest["unit"]})
        return jsonify({"receipe": receipeToSend, "ingredients": ingredients})
    
    @app.route("/receipes/<int:id>", methods=["DELETE"])
    @cross_origin()
    def delete_receipe(id):
        ingredientMap = ingredientsPerReceipe.query.filter_by(receipe_id = id)
        [ingr.delete() for ingr in ingredientMap]
        receipe = Receipes.query.get(id)
        receipe.delete()
        return jsonify({"success": True})

    @app.route("/receipes/<int:id>", methods=["PATCH"])
    @cross_origin()
    def update_receipe(id):
        try:
            inputData = request.get_json()
            ingredientMap = ingredientsPerReceipe.query.filter_by(receipe_id = id)
            [ingr.delete() for ingr in ingredientMap]
            receipe = Receipes.query.get(id)
            print("found receipe: ", receipe)
            receipe.update(name = inputData["name"], description = inputData["receipe"])
            for ingredient in inputData["ingredients"]:
                    existingIngredient = Ingredient.query.filter(Ingredient.name.ilike(ingredient["name"]), Ingredient.unit.ilike(ingredient["unit"])).one_or_none()
                    if existingIngredient:
                        ingredientId = existingIngredient.id
                    else:
                        newIngredient = Ingredient(name=ingredient["name"], unit=ingredient["unit"])
                        newIngredient.insert()
                        ingredientId = newIngredient.id
                    newIngredientMap = ingredientsPerReceipe(ingredient_id=ingredientId, receipe_id=id, amount=ingredient["amount"])
                    newIngredientMap.insert()
            return jsonify({"success": True})
        except:
            abort (400)

        

        return jsonify({"success": True})
        
    @app.errorhandler(400)
    def err_bad_request(error):
        return jsonify({
            "success": False,
            "message": "The request was not formatted correctly",
            "error": 400
        }), 400

    @app.errorhandler(404)
    def err_not_found(error):
        return jsonify({
            "success": False,
            "message": "The requested resource could not be found",
            "error": 404
        }), 404
    
    @app.errorhandler(422)
    def err_not_processable(error):
        return jsonify({
            "success": False,
            "message": "The request could not be processed",
            "error": 422
        }), 422
    
    @app.errorhandler(500)
    def err_internal(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong on serverside",
            "error": 500
        }), 500
    
    return app