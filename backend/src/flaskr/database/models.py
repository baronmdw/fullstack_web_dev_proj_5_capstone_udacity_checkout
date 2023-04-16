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
            }