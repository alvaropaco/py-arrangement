import datetime

from flask import Flask, jsonify, json, url_for, redirect, request
from flask.ext.api import status
from flask_pymongo import PyMongo, MongoClient
from flask_restful import fields, marshal, marshal_with, reqparse, Resource
from bson import json_util
from bson.objectid import ObjectId
from urllib import quote_plus

from ..common.JSONEncoder import JSONEncoder

APP_URL = "http://127.0.0.1:8080"

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title', dest='title',
    location='json', required=True,
    help='title is required',
)
post_parser.add_argument(
    'room', dest='room',
    location='json', required=True, 
    help='room is required',
)
post_parser.add_argument(
    'start_at', dest='startAt',
    location='json', required=True,
    help='start_at is required',
)
post_parser.add_argument(
    'end_at', dest='endAt',
    location='json',
    help='The end datetime',
)
post_parser.add_argument(
    'created_at', dest='createdAt',
    location='json',
    help='Creation',
)
post_parser.add_argument(
    'upadated_at', dest='updatedAt',
    location='json',
    help='Last update',
)


arrange_fields = {
    "endAt": fields.String(attribute='end_at'),
    "id": fields.String,
    "room": fields.String,
    "startAt": fields.String(attribute='start_at'),
    "title": fields.String,
    "createdAt": fields.String(attribute='created_at'),
    "updatedAt": fields.String(attribute='updated_at')
}

created_arrangement_response = {
    '_id': fields.String
}


class Arrange(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, id=None, range=None):
        data = []

        if request.args:
            data = request.args
        
        if id is None and data and data['id']:
            id = data['id']
        
        if id:
            arrange_info = self.db.arrange.find_one({"_id": ObjectId(id)})
            if arrange_info:
                return jsonify(marshal(json_util._json_convert(arrange_info), arrange_fields))
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

    @marshal_with(created_arrangement_response)
    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            data['created_at'] = datetime.datetime.now()
            arrange = self.db.arrange.insert_one(data)
            return {
                "_id": str(arrange.inserted_id)
            }, status.HTTP_201_CREATED

    @marshal_with(arrange_fields)
    def put(self):
        data = request.get_json()
        data['updated_at'] = datetime.datetime.now()

        q = {"_id": ObjectId(data['id'])}

        self.db.arrange.update(q, {'$set': data})
        updated_arrangement = self.db.arrange.find_one(q)
        return data

    def delete(self, id):
        self.db.arrange.remove({'id': id})
        return redirect(url_for("arrange"))
