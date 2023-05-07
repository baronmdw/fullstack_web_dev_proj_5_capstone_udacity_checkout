import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
database_path = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)


db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

class Connectiontest(db.Model):
    __tablename__ = "connectiontest"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    test2 = Column(String)

    # def __init__(self, question, answer, category, difficulty):
    #     self.question = question
    #     self.answer = answer
    #     self.category = category
    #     self.difficulty = difficulty

    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
        # db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'text': self.text,
            'probablyempty': self.test2
            }
    
class ingredientsPerReceipe (db.Model):
    __tablename__ = "ingredientmap"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    receipe_id = Column(Integer, db.ForeignKey("receipes.id"), nullable=False)
    ingredient_id = Column(Integer, db.ForeignKey("ingredients.id"), nullable=False)
    # receipe = db.relationship("Receipes", backref=db.backref("receipe_ingredientmap", lazy=True))
    # ingredient = db.relationship("Ingredient", backref=db.backref("ingredient_ingredientmap", lazy=True))
    
    def __init__(self, receipe_id, ingredient_id, amount):
        self.receipe_id = receipe_id
        self.ingredient_id = ingredient_id
        self.amount = amount

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "receipe_id": self.receipe_id,
            "ingredient_id": self.ingredient_id
        }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
                                 

class Receipes(db.Model):
    __tablename__ = "receipes"

    id =  Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    # ingredient = db.relationship("Ingredient", secondary="ingredientsPerReceipe", backref=db.backref("receipe", lazy=True), overlaps="ingredient, ingredientmap")

    # genres = db.relationship('Genre', secondary=Genremap, backref=db.backref('artist', lazy=True), overlaps="genres,venue")
        # artist = db.relationship('Artist', secondary='Show', backref=db.backref('venue', lazy=True), overlaps="venue,venue_shows")



    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    # def update(self):
    #     db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    unit = Column(String)

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return{
            "id": self.id,
            "name": self.name,
            "unit": self.unit
        }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Genremap = db.Table('Genremap',
#                     db.Column('id', db.Integer, primary_key=True),
#                     db.Column('venue_id',db.Integer, db.ForeignKey('Venue.id'), nullable=True),
#                     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), nullable=True),
#                     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), nullable=False)
#                     )
