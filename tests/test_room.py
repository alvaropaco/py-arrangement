# -*- coding: utf-8 -*-
import json
import requests
import unittest
from bson import json_util
from jsonschema import validate
from ..api.app import app
from ..api.common.json2obj import json2obj

responde_schema = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"}
    }
}

room_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "room": {"type": "string"},
        "start_at": {"type": "string"},
        "end_at": {"type": "string"}
    },
}

class RoomTestCase(unittest.TestCase):
    """This class represents the room test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()

    def test_room_creation_happy_flow(self):
        """Test API can create a new Room (POST request)"""
        room = {
            "room": "Reuniao X",
            "code": "ABC123"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/room',
                            data=json.dumps(room), 
                            content_type='application/json')

        data = json.loads(res.data)

        self.room_id = data['_id']

        self.assertEqual(res.status_code, 201)
        self.assertIsNone(validate(data, responde_schema))

    def test_room_updating_happy_flow(self):
        room = {
            "room": "Teste",
            "code": "ABC123",
        }

        res = self.app.post('http://127.0.0.1:5000/v1/room',
                            data=json.dumps(room), content_type='application/json')

        data = json.loads(res.data)

        room_id = data['_id']

        room = {
            "id": room_id,
            "room": "Updated",
            "code": "ABC123",
        }

        res = self.app.put('http://127.0.0.1:5000/v1/room',
                           data=json.dumps(room), 
                           content_type='application/json')
        data = json2obj(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.room, "Updated")

    def test_room_creation_unhappy_flow(self):
        """Test API can create a roomment (POST request)"""
        room = {
            "room": "roomment Test Title",
            "code": "ABC123"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/room', data=room)

        data = json_util._json_convert(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, str('{"_id": null}\n'))

    def test_room_get_by_id_happy_flow(self):
        """Test API can create a roomment (POST request)"""

        room = {
            "room": "Teste",
            "code": "ABC123"
        }

        res = self.app.post('http://127.0.0.1:5000/v1/room',
                            data=json.dumps(room), content_type='application/json')

        data = json.loads(res.data)

        room_id = data['_id']

        res = self.app.get(
            'http://127.0.0.1:5000/v1/room/{id}'.format(id=room_id))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNone(validate(data, room_schema))

    def test_room_remove_by_id_happy_flow(self):
        """Test API can create a roomment (POST request)"""

        room = {
            "room": "Teste",
            "code": "ABC123",
        }

        res = self.app.post('http://127.0.0.1:5000/v1/room',
                            data=json.dumps(room), content_type='application/json')

        data = json.loads(res.data)

        room_id = data['_id']

        res = self.app.delete(
            'http://127.0.0.1:5000/v1/room/{id}'.format(id=room_id))

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
