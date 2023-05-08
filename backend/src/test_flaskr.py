import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import upgrade

from flaskr import create_app
from flaskr.database.models import setup_db, Connectiontest

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.DB_TEST_HOST = os.environ.get("DB_HOST")
        self.DB_TEST_USER = os.environ.get("DB_USER")
        self.DB_TEST_PASSWORD = os.environ.get("DB_PASSWORD")
        self.DB_TEST_NAME = os.environ.get("DB_TEST_NAME")
        self.DB_TEST_PORT = os.environ.get("DB_PORT")
        self.database_path = 'postgresql://{}:{}@{}:{}/{}'.format(self.DB_TEST_USER,self.DB_TEST_PASSWORD,self.DB_TEST_HOST, self.DB_TEST_PORT, self.DB_TEST_NAME)
        print(self.database_path)
        self.app = create_app(self.database_path)
        with self.app.app_context():
            upgrade()
        self.client = self.app.test_client
   
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_hello(self):
        # This test tests for general health status of the server
        res = self.client().get("/")
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content[0].keys()), 1)

    def test_get_receipes(self):
        # This test tests for the correct transmission of all categories
        res = self.client().get("/receipes")
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content["receipes"].keys()), 1)

    # TODO: def test_get_receipes_unauthorized(self):
        #this test checks if an unauthorized user will be neglected to receive receipes

    #TODO: def test_post_receipes(self):
        # This test checks if adding a receipe via post request will work
    
    #TODO: def test_post_receipes_unauthorized(self):
        # This test checks if a user will fail to post a receipe without being authorized

    #TODO: def test_get_single_receipe(self):
        # This test checks if getting a single receipes details works correctly
    
    #TODO: def test_get_single_receipe_wrong_id(self):
        # This test checks if trying to access a non-existent receipe will result in an error

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()