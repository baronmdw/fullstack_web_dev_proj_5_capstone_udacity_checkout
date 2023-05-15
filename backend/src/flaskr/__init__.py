import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from .database.models import setup_db, Connectiontest, Receipes, Ingredient, ingredientsPerReceipe, db
from flask_migrate import Migrate
from .auth.auth import AuthError, requires_auth

#Setup App
def create_app(dbURI='', test_config=None):
    # read environment variables if not in Testmode
    if dbURI == "":
        if os.environ.get("FLASK_DEBUG") == "1": 
            print("debugging: ", os.environ.get("FLASK_DEBUG"))  
            DB_HOST = os.environ.get("DB_HOST")
            DB_USER = os.environ.get("DB_USER")
            DB_PASSWORD = os.environ.get("DB_PASSWORD")
            DB_NAME = os.environ.get("DB_NAME")
            DB_PORT = os.environ.get("DB_PORT")
            dbURI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
        else:
            DB_URL = os.environ.get("DB_URL")
            dbURI = DB_URL

    #initialize app   
    app = Flask(__name__)
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=dbURI)

    #setup database connection
    setup_db(app, dbURI)
    Migrate(app,db)

    #enable cors
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)

    #this endpoint serves to make a healthcheck of the server including the database
    @app.route("/")
    @cross_origin()
    def index(payload):
        #connectiontest model just serves for checking the health
        connections = Connectiontest.query.all()
        connections_formatted = [c.format() for c in connections]
        #return the content of the connectiontest table
        return (connections_formatted)
    
    #this endpoint serves to get all receipes included in the database on a high level
    @app.route("/receipes", methods=["GET", "OPTIONS"])
    #TODO: enable authorization check, read role
    #TODO: errorhandling
    @requires_auth("get:receipes")
    @cross_origin()
    def get_receipes(payload):
        if request.method == "OPTIONS":
            return jsonify("OK")
        elif request.method == "GET":
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
    @app.route("/receipes", methods=["POST", "OPTIONS"])
    #TODO: enable authorization check, create role
    #TODO: better errorhandling
    @requires_auth("post:receipes")
    @cross_origin()
    def post_receipe(payload):
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
    
    #this endpoint serves to get the details of one receipe
    @app.route("/receipes/<int:id>", methods=["GET", "OPTIONS"])
    #TODO: authorizationcheck, read role
    #TODO: errorhandling
    @requires_auth("get:receipes")
    @cross_origin()
    def get_receipe(payload,id):
        #query the receipe from the database and format it
        receipe = Receipes.query.get(id)
        receipeToSend = receipe.format()
        #query the ingredient ids and amounts connected to the receipe and format them
        ingredientMap = ingredientsPerReceipe.query.filter_by(receipe_id = id)
        ingredientMapFormatted = [item.format() for item in ingredientMap]
        ingredients = []
        #get the ingredient name and unit and put it to the ingredient object array
        for ingredientMapElement in ingredientMapFormatted:
            ingredientToAdd = Ingredient.query.get(ingredientMapElement["ingredient_id"])
            ingredientOfInterest = ingredientToAdd.format()
            ingredients.append({"id": ingredientOfInterest["id"], "name": ingredientOfInterest["name"], "amount": ingredientMapElement["amount"], "unit": ingredientOfInterest["unit"]})
        return jsonify({"receipe": receipeToSend, "ingredients": ingredients})
    
    #this endpoint serves to delete a specific receipe item
    @app.route("/receipes/<int:id>", methods=["DELETE", "OPTIONS"])
    #TODO: authorization, create role
    #TODO: errorhandling
    @requires_auth("delete:receipes")
    @cross_origin()
    def delete_receipe(payload,id):
        #query the ingredientsmapping objects that belong to the receipe item and delete each one of them
        ingredientMap = ingredientsPerReceipe.query.filter_by(receipe_id = id)
        [ingr.delete() for ingr in ingredientMap]
        #query the receipe object and delete it
        receipe = Receipes.query.get(id)
        receipe.delete()
        return jsonify({"success": True})
    
    #this endpoint serves to change a receipe item
    @app.route("/receipes/<int:id>", methods=["PATCH", "OPTIONS"])
    #TODO: authorization, create role
    #TODO: errorhandling
    @requires_auth("patch:receipe")
    @cross_origin()
    def update_receipe(payload,id):
        try:
            #get the input data object, query all ingredients belonging to the receipe and delete them
            inputData = request.get_json()
            ingredientMap = ingredientsPerReceipe.query.filter_by(receipe_id = id)
            [ingr.delete() for ingr in ingredientMap]
            #query the receipe object and update the name and description
            receipe = Receipes.query.get(id)
            receipe.update(name = inputData["name"], description = inputData["receipe"])
            #create the new ingredientmapping objects depending on existing ingredient item or new one
            for ingredient in inputData["ingredients"]:
                    #check if ingredient item exists
                    existingIngredient = Ingredient.query.filter(Ingredient.name.ilike(ingredient["name"]), Ingredient.unit.ilike(ingredient["unit"])).one_or_none()
                    if existingIngredient:
                        #existing item
                        ingredientId = existingIngredient.id
                    else:
                        #new item
                        newIngredient = Ingredient(name=ingredient["name"], unit=ingredient["unit"])
                        newIngredient.insert()
                        ingredientId = newIngredient.id
                    #ingredient mapping object
                    newIngredientMap = ingredientsPerReceipe(ingredient_id=ingredientId, receipe_id=id, amount=ingredient["amount"])
                    newIngredientMap.insert()
            #TODO: reply with newly created object
            return jsonify({"success": True})
        except:
            abort (400)


    #Definition of errorhandlers for the errors defined in the app 
    
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