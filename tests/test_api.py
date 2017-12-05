# ================================================== #
#                     PROCESSOR                      #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 12/04/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #


from app.api.api import ReputationAPI
from app.storage.storage import Data
import falcon
from falcon import testing
try:
    import ujson as json
except ImportError:
    import json
import unittest


# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #


class APITestCase(testing.TestCase):
    def setUp(self):
        super(APITestCase, self).setUp()
        self.app = falcon.API()
        api = ReputationAPI(mode="Development")
        self.app.add_route('/reputation/', api)
        self.app.add_route('/reputation/{reputee}', api)

    # ============================================= #

    def tearDown(self):
        super(APITestCase, self).tearDown()
        data = Data("Development")
        data.open()
        data.clear()
        data.close()


# ================================================== #


class TestAPI(APITestCase):
    def test_post_no_json(self):
        result = self.simulate_post('/reputation')
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"title":"Error","description":"A valid JSON document is required."}')

    # ============================================= #

    def test_post_empty_json(self):
        result = self.simulate_post('/reputation', body=json.dumps({}), headers = {"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"title":"Malformed JSON","description":"Could not decode the request body. '
                                      'The JSON was formatted incorrectly."}')

    # ============================================= #

    def test_post_misformatted_json(self):
        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test","reputee": "Test","wrong_key":
                                    {"rid" : "44cd865e-d987-11e7-9296-cec278b6b50a","feature": "clarity","value": 10}}),
                                    headers = {"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"title":"Malformed JSON","description":"Could not decode the request body. '
                                      'The JSON was formatted incorrectly."}')

    # ============================================= #

    def test_post_normal(self):
        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "44cd865e-d987-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 10}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-44cd865e-d987-11e7-9296-cec278b6b50a successfully created."}')

    # ============================================= #

    def test_post_normal_repeat(self):
        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "44cd865e-d987-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 10}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-44cd865e-d987-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "44cd865e-d987-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 10}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, '{"message":"rid-44cd865e-d987-11e7-9296-cec278b6b50a already exists."}')

    # ============================================= #

    def test_get_no_reputee(self):
        result = self.simulate_get('/reputation')
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"title":"Error","description":"A valid query is required."}')

    # ============================================= #

    def test_get_reputee_not_found(self):
        result = self.simulate_get('/reputation/Test_String')
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"title":"Error","description":"Reputee could not be found."}')

    # ============================================= #

    def test_get_normal(self):
        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21ce02-d98a-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 10}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21ce02-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d078-d98a-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 8}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d078-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d186-d98a-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 8}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d186-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d4b0-d98a-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 7}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d4b0-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d5c8-d98a-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 9}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d5c8-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d6b8-d98a-11e7-9296-cec278b6b50a", "feature": "clarity", "value": 8}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d6b8-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d79e-d98a-11e7-9296-cec278b6b50a", "feature": "reach", "value": 4}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d79e-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d87a-d98a-11e7-9296-cec278b6b50a", "feature": "reach", "value": 5}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d87a-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21d956-d98a-11e7-9296-cec278b6b50a", "feature": "reach", "value": 4}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21d956-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_post('/reputation', body=json.dumps({"reputer": "Test", "reputee": "Test", "repute":
            {"rid": "7a21dcc6-d98a-11e7-9296-cec278b6b50a", "feature": "reach", "value": 5}}),
                                    headers={"Content-Type": "application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.text, '{"message":"rid-7a21dcc6-d98a-11e7-9296-cec278b6b50a successfully created."}')

        result = self.simulate_get('/reputation/Test')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, '{"reputee":"Test","clout":{"score":0.6416666667,"confidence":0.5},"reach":{"score":4.5,"confidence":0.5},"clarity":{"score":8.3333333333,"confidence":0.5}}')


# ================================================== #


if __name__  == '__main__':
    unittest.main()


# ================================================== #
#                        EOF                         #
# ================================================== #
