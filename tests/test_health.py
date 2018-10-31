# -*- coding: utf-8 -*-
import json
import unittest
from jsonschema import validate
from ..api.app import app
from ..api.common.json2obj import json2obj

responde_schema = {
    "type": "object",
    "properties": {
        "response": {"type": "string", "value": "health"}
    }
}

class RoomTestCase(unittest.TestCase):
    """This class represents the room test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()

    def test_health(self):
        """Test API health"""
        

        res = self.app.get('http://127.0.0.1:5000/v1')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNone(validate(data, responde_schema))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
