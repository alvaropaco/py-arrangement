# -*- coding: utf-8 -*-
import unittest
import requests
from bson import json_util
import json
from jsonschema import validate

from ..api.app import app
from ..api.common.json2obj import json2obj

responde_schema = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"}
    }
}

arrange_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "room": {"type": "string"},
        "start_at": {"type": "string"},
        "end_at": {"type": "string"}
    },
}


class ArrangeTestCase(unittest.TestCase):
    """This class represents the arrange test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()

    def test_arrange_creation_happy_flow(self):
        """Test API can create a arrangement (POST request)"""
        arrange = {
            "title": "Teste",
            "room": "ABC123",
            "start_at": "2018-10-29T23:29:09.479878",
            "end_at": "2018-11-29T23:29:09.479878"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/arrange',
                            data=json.dumps(arrange),
                            content_type='application/json')

        data = json.loads(res.data)

        self.arrange_id = data['_id']

        self.assertEqual(res.status_code, 201)
        self.assertIsNone(validate(data, responde_schema))

    def test_arrange_updating_happy_flow(self):
        arrange = {
            "title": "Teste",
            "room": "ABC123",
            "start_at": "2018-10-29T23:29:09.479878",
            "end_at": "2018-11-29T23:29:09.479878"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/arrange',
                            data=json.dumps(arrange), 
                            content_type='application/json')

        data = json.loads(res.data)

        arrange_id = data['_id']

        arrange = {
            "id": arrange_id,
            "title": "Updated",
            "room": "ABC123",
            "start_at": "2018-10-29T23:29:09.479878",
            "end_at": "2018-11-29T23:29:09.479878"
        }

        res = self.app.put('http://127.0.0.1:5000/v1/arrange',
                           data=json.dumps(arrange), 
                           content_type='application/json')

        data = json2obj(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.title, "Updated")

    def test_arrange_creation_unhappy_flow(self):
        """Test API can create a arrangement (POST request)"""
        arrange = {
            "title": "Arrangement Test Title",
            "room": "ABC123",
            "start_at": 1349960286,
            "end_at": 1349960286
        }

        res = self.app.post('http://127.0.0.1:5000/v1/arrange', data=arrange)

        data = json_util._json_convert(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, str('{"_id": null}\n'))

    def test_arrange_list_happy_flow(self):
        """Test API can create a arrangement (POST request)"""

        res = self.app.get('http://127.0.0.1:5000/v1/arrange')

        data = json_util._json_convert(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data) > 1)

    def test_arrange_get_by_id_happy_flow(self):
        """Test API can create a arrangement (POST request)"""

        arrange = {
            "title": "Teste",
            "room": "ABC123",
            "start_at": "2018-10-29T23:29:09.479878",
            "end_at": "2018-11-29T23:29:09.479878"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/arrange',
                            data=json.dumps(arrange), content_type='application/json')

        data = json.loads(res.data)

        arrange_id = data['_id']

        res = self.app.get(
            'http://127.0.0.1:5000/v1/arrange/{id}'.format(id=arrange_id))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNone(validate(data, arrange_schema))

    def test_arrange_remove_by_id_happy_flow(self):
        """Test API can create a arrangement (POST request)"""

        arrange = {
            "title": "Teste",
            "room": "ABC123",
            "start_at": "2018-10-29T23:29:09.479878",
            "end_at": "2018-11-29T23:29:09.479878"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/arrange',
                            data=json.dumps(arrange), content_type='application/json')

        data = json.loads(res.data)

        arrange_id = data['_id']

        res = self.app.delete(
            'http://127.0.0.1:5000/v1/arrange/{id}'.format(id=arrange_id))

        self.assertEqual(res.status_code, 200)

    # def tearDown(self):
    #     """teardown all initialized variables."""
    #     self.app.app_context():
    #         # drop all tables
    #         db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
