from datetime import datetime
import time
import dateutil.parser

from flask import Flask, jsonify, json, url_for, redirect, request
from flask_pymongo import PyMongo, MongoClient
from flask_restful import fields, marshal, marshal_with, reqparse, Resource
from bson import json_util
from bson.objectid import ObjectId
from urllib import quote_plus

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
    "endAt": fields.Float(attribute='end_at'),
    "id": fields.String(attribute='_id.$oid'),
    "room": fields.String,
    "startAt": fields.Float(attribute='start_at'),
    "title": fields.String,
    "createdAt": fields.Float(attribute='created_at'),
    "updatedAt": fields.Float(attribute='updated_at')
}

created_arrangement_response = {
    '_id': fields.String
}


def getTimestamp(dt):
    return round(time.mktime(dt.timetuple()) + dt.microsecond/1e6)


class Arrange(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @marshal_with(arrange_fields)
    def get(self, id=None):
        data = []

        if request.args:
            data = request.args

        if id is not None:
            arrange_info = self.db.arrange.find_one({"_id": ObjectId(id)})
            if arrange_info:
                return json_util._json_convert(arrange_info)
            else:
                return {"response": "no arrange found for {}".format(id)}

        if data:
            start_timestamp = float(data['start'])
            end_timestamp = float(data['end'])

            query = {
                "$or": [
                    {"start_at": {
                        "$gte": start_timestamp,
                        "$lt": end_timestamp
                    }},
                    {"end_at": {
                        "$gte": start_timestamp,
                        "$lt": end_timestamp
                    }}
                ]
            }

            cursor = self.db.arrange.find(query).limit(25)

            respond = []

            for arrange in cursor:
                arrangeObj = json_util._json_convert(arrange)
                respond.append(arrangeObj)

            return respond

        cursor = self.db.arrange.find({}).limit(50)

        respond = []

        for arrange in cursor:
            arrangeObj = json_util._json_convert(arrange)
            respond.append(arrangeObj)

        return respond

    @marshal_with(created_arrangement_response)
    def post(self):
        data = request.get_json()

        if not data:
            data = {"response": "ERROR"}
            return jsonify(data), 400
        else:
            data['created_at'] = getTimestamp(datetime.utcnow())

            startAt = getTimestamp(dateutil.parser.parse(data['start_at']))
            endAt = getTimestamp(dateutil.parser.parse(data['end_at']))

            data['start_at'] = startAt
            data['end_at'] = endAt

            arrange = self.db.arrange.insert_one(data)
            return {
                "_id": str(arrange.inserted_id)
            }, 201

    @marshal_with(arrange_fields)
    def put(self):
        data = request.get_json()

        startAt = getTimestamp(dateutil.parser.parse(data['start_at']))
        endAt = getTimestamp(dateutil.parser.parse(data['end_at']))
        updatedAt = getTimestamp(datetime.now())

        data['start_at'] = startAt
        data['end_at'] = endAt
        data['updated_at'] = updatedAt

        q = {"_id": ObjectId(data['id'])}

        self.db.arrange.update(q, {'$set': data})

        self.db.arrange.find_one(q)

        return data

    def delete(self, id):
        self.db.arrange.remove({"_id": ObjectId(id)})
        return {}, 200
