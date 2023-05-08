import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from .database.models import setup_db, Connectiontest, Receipes, Ingredient, ingredientsPerReceipe, db
from flask_migrate import Migrate

#Setup App
def create_app(dbURI='', test_config=None):
    # read environment variables if not in Testmode
    if dbURI == "":
        DB_HOST = os.environ.get("DB_HOST")
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_NAME = os.environ.get("DB_NAME")
        DB_PORT = os.environ.get("DB_PORT")
        dbURI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

    #initialize app   
    app = Flask(__name__)
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=dbURI)

    #setup database connection
    setup_db(app, dbURI)
    Migrate(app,db)

    #enable cors
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    #this endpoint serves to make a healthcheck of the server including the database
    @app.route("/")
    @cross_origin()
    def index():
        #connectiontest model just serves for checking the health
        connections = Connectiontest.query.all()
        connections_formatted = [c.format() for c in connections]
        #return the content of the connectiontest table
        return (connections_formatted)
    
    #this endpoint serves to get all receipes included in the database on a high level
    @app.route("/receipes", methods=["GET"])
    #TODO: enable authorization check, read role
    #TODO: errorhandling
    @cross_origin()
    def get_receipes():
        #query all receipes and format them for readability in the frontend
        receipes = Receipes.query.all()
        receipes_formatted = [r.format() for r in receipes]
        #create responseobject with successstats and the formatted receipelist
        responseObject = {
            "success": True,
            "receipes": receipes_formatted
        }
        return jsonify(responseObject)

    #this endpoint serves to post a new receipe to the database
    @app.route("/receipes", methods=["POST"])
    #TODO: enable authorization check, create role
    #TODO: better errorhandling
    @cross_origin()
    def post_receipe():
        #get content of the request
        inputReceipe = request.get_json()
        try:
            #add a new receipe object
            newReceipe = Receipes(name=inputReceipe["name"], description=inputReceipe["receipe"])
            newReceipe.insert()
            #loop through ingeredients, check if engredient type already exists, add it if necessary and add mappingobject
            for ingredient in inputReceipe["ingredients"]:
                existingIngredient = Ingredient.query.filter(Ingredient.name.ilike(ingredient["name"]), Ingredient.unit.ilike(ingredient["unit"])).one_or_none()
                if existingIngredient:
                    #work with existing ingredient
                    ingredientId = existingIngredient.id
                else:
                    #create new ingredient
                    newIngredient = Ingredient(name=ingredient["name"], unit=ingredient["unit"])
                    newIngredient.insert()
                    ingredientId = newIngredient.id
                #add mappingobject
                newIngredientMap = ingredientsPerReceipe(ingredient_id=ingredientId, receipe_id=newReceipe.id, amount=ingredient["amount"])
                newIngredientMap.insert()
            #TODO: add new object id to response
            return jsonify({"success": True})
        except:
            db.session.rollback()
            abort(400)
    
    #
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