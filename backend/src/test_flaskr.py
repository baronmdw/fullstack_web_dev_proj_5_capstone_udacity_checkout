import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import upgrade
from unittest.mock import patch

from flaskr import create_app
from flaskr.database.models import setup_db, Connectiontest

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    # def mockenv(**envvars):
    #     return mock.patch.dict(os.environ, envvars)

    # @mockenv(AUTH0_DOMAIN=os.environ.get("AUTH0_DOMAIN"))
    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.DB_TEST_HOST = os.environ.get("DB_HOST")
        self.DB_TEST_USER = os.environ.get("DB_USER")
        self.DB_TEST_PASSWORD = os.environ.get("DB_PASSWORD")
        self.DB_TEST_NAME = os.environ.get("DB_TEST_NAME")
        self.DB_TEST_PORT = os.environ.get("DB_PORT")
        self.database_path = 'postgresql://{}:{}@{}:{}/{}'.format(self.DB_TEST_USER,self.DB_TEST_PASSWORD,self.DB_TEST_HOST, self.DB_TEST_PORT, self.DB_TEST_NAME)

        self.write_user = [os.environ.get("email_foodplanner"), os.environ.get("pwd_foodplanner")]
        self.read_user = [os.environ.get("email_reader"), os.environ.get("pwd_reader")]
       
        self.write_user_jwt = os.environ.get("WRITE_JWT")
        self.read_user_jwt = os.environ.get("READ_JWT")
        self.test_config = {
            "AUTH0_DOMAIN" : os.environ.get("AUTH0_DOMAIN"),
            "ALGORITHMS" : [os.environ.get("ALGORITHMS")],
            "API_AUDIENCE" : os.environ.get("API_AUDIENCE")
        }
        self.new_id = None


        self.app = create_app(self.database_path, self.test_config)
        with self.app.app_context():
            upgrade()
        self.client = self.app.test_client
   


    def tearDown(self):
        """Executed after each test"""
        pass

    def test_00_get_hello(self):
        # This test tests for general health status of the server
        res = self.client().get("/")
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content[0].keys()), 1)

    def test_01_post_receipes(self):
        # This test checks if adding a receipe via post request will work
        new_element = {
            "name": "Test Receipe",
            "receipe": "Add some testing",
            "ingredients": [{"name": "Test Ingredient", "unit": "Test Unit", "amount": 1}]
        }
        res = self.client().post("/receipes", json=new_element, headers={"Authorization": 'Bearer {}'.format(self.write_user_jwt)})
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(content["success"], True)
    
    def test_02_post_receipes_unauthorized(self):
        # This test checks if a user will fail to post a receipe without being authorized
        new_element = {
            "name": "Test Receipe",
            "receipe": "Add some testing",
            "ingredients": [{"name": "Test Ingredient", "unit": "Test Unit", "amount": 1}]
        }
        res = self.client().post("/receipes", json=new_element)
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(content["success"], False)

    def test_03_get_receipes(self):
        # This test tests for the correct transmission of all categories
        res = self.client().get("/receipes", headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content["receipes"]), 1)

    def test_04_get_receipes_unauthorized(self):
        #this test checks if an unauthorized user will be neglected to receive receipes
        res = self.client().get("/receipes")
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(content["message"]["code"], "invalid header")

    def test_05_get_single_receipe(self):
        # This test checks if getting a single receipes details works correctly
        res = self.client().get('/receipes', headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        new_id = content["receipes"][-1]["id"]
        res = self.client().get('/receipes/{}'.format(new_id), headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Test Receipe",content["receipe"]["name"])
    
    def test_06_get_single_receipe_wrong_id(self):
        # This test checks if trying to access a non-existent receipe will result in an error
        res = self.client().get('/receipes', headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        nonexisting_id = content["receipes"][-1]["id"]+100
        res = self.client().get('/receipes/{}'.format(nonexisting_id), headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(content["success"], False)
        
    def test_07_patch_receipe(self):
        # This test checks if updating a receipe works
        res = self.client().get('/receipes', headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        new_id = content["receipes"][-1]["id"]
        update_data={
            "name": "Updated Test Receipe",
            "receipe": "Add some more testing",
            "ingredients": [{"name": "Test Ingredient", "unit": "Test Unit", "amount": 1}, {"name": "Second Test Ingredient", "unit": "Test Unit", "amount": 2}]
        }
        res = self.client().patch('/receipes/{}'.format(new_id), headers={"Authorization": 'Bearer {}'.format(self.write_user_jwt)}, json=update_data)
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(content["id"], new_id)


    def test_08_patch_receipe_wrong(self):
        # This test checks if updating a receipe with wrong input results in an error
        res = self.client().get('/receipes', headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        new_id = content["receipes"][-1]["id"]+100
        update_data={
            "name": "Updated Test Receipe",
            "receipe": "Add some more testing",
        }
        res = self.client().patch('/receipes/{}'.format(new_id), headers={"Authorization": 'Bearer {}'.format(self.write_user_jwt)}, json=update_data)
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(content["success"], False)

    def test_09_delete_receipe(self):
        # This test checks if deleting a receipe works
        res = self.client().get('/receipes', headers={"Authorization": 'Bearer {}'.format(self.read_user_jwt)})
        content = json.loads(res.data)
        new_id = content["receipes"][-1]["id"]
        res = self.client().delete('/receipes/{}'.format(new_id), headers={"Authorization": 'Bearer {}'.format(self.write_user_jwt)})
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(content["success"], True)

    def test_10_delete_receipe_not_existing(self):
        # This test checks if deleting a non-existing receipe will result in an error
        new_id = 1
        res = self.client().delete('/receipes/{}'.format(new_id), headers={"Authorization": 'Bearer {}'.format(self.write_user_jwt)})
        content = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(content["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()