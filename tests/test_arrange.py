# -*- coding: utf-8 -*-
import unittest
import requests
from bson import json_util

from ..api.app import app

class ArrangeTestCase(unittest.TestCase):
    """This class represents the arrange test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()
        self.arrange = {'name': 'Arrangements'}

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

    # def tearDown(self):
    #     """teardown all initialized variables."""
    #     with self.app.app_context():
    #         # drop all tables
    #         db.session.remove()
    #         db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()