from flask import Flask, jsonify, json, url_for, redirect, request
from flask_pymongo import PyMongo, MongoClient
from flask_restful import fields, marshal_with, reqparse, Resource
from bson import json_util
from bson.objectid import ObjectId
from urllib import quote_plus

APP_URL = "http://127.0.0.1:8080"

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title', dest='title',
    location='json', required=True,
    help='The Arrangement\'s title',
)
post_parser.add_argument(
    'room', dest='room',
    location='json', required=True, 
    help='The room\'s code',
)
post_parser.add_argument(
    'start_at', dest='startAt',
    location='json',
    help='The start datetime',
)
post_parser.add_argument(
    'end_at', dest='endAt',
    location='json',
    help='The end datetime',
)

arrange_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'room': fields.String,
    'startAt': fields.DateTime,
    'endAt': fields.DateTime,
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime
}


class Arrange(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, id=None, range=None, emotion=None):
        data = request.args

        if id is None:
            id = data['id']

        if id:
            arrange_info = self.db.arrange.find_one({"_id": ObjectId(id)})
            if arrange_info:
                return jsonify({"status": "ok", 
                "data": json.dumps(arrange_info, default=json_util.default)})
            else:
                return {"response": "no arrange found for {}".format(id)}

        elif range:
            #YYYYMMDDHHMMSS
            range = range.split('to')
            cursor = self.db.arrage.find({"timestamp":{"$gt": int(range[0])}, "timestamp":{"$lt": int(range[1])}}, {"_id": 0}).limit(10)
            for arrange in cursor:
                data.append(arrange)

            return jsonify({"range": range, "response": data})
        else:
            cursor = self.db.arrange.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for arrange in cursor:
                data.append(arrange)

            return jsonify({"response": data})

    @marshal_with(arrange_fields)
    def post(self):
        data = post_parser.parse_args()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            arrange = self.db.arrange.insert(data)
            return arrange

    def put(self, id):
        data = request.get_json()
        self.db.arrange.update({'id': id}, {'$set': data})
        return redirect(url_for("arrange"))

    def delete(self, id):
        self.db.arrange.remove({'id': id})
        return redirect(url_for("arrange"))
