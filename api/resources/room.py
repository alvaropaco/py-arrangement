from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
from time import mktime

from flask import Flask, jsonify, request
from flask_restful import fields, marshal_with, reqparse, Resource

from ..common.timestamp import fromDateTime

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'room', dest='room',
    location='json', required=True,
    help='room name is required',
)
post_parser.add_argument(
    'code', dest='code',
    location='json', required=True,
    help='code is required',
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

room_fields = {
    "room": fields.String,
    "code": fields.String,
    "createdAt": fields.Float(attribute='created_at'),
    "updatedAt": fields.Float(attribute='updated_at')
}

created_room_response = {
    '_id': fields.String
}

def getTimestamp(dt):
    return round(mktime(dt.timetuple()) + dt.microsecond/1e6)


class Room(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @marshal_with(room_fields)
    def get(self, id=None):

        if id is not None:
            room_info = self.db.room.find_one({"_id": ObjectId(id)})
            if room_info:
                return json_util._json_convert(room_info)

        return {"response": "no room found for {}".format(id)}

    @marshal_with(created_room_response)
    def post(self):
        data = request.get_json()

        if not data:
            data = {"response": "ERROR"}
            return jsonify(data), 400
        else:
            data['created_at'] = getTimestamp(datetime.utcnow())

            room = self.db.room.insert_one(data)
            return {
                "_id": str(room.inserted_id)
            }, 201

    @marshal_with(room_fields)
    def put(self):
        data = request.get_json()

        if data['id'] is None:
            data = {"response": "ERROR"}
            return jsonify(data), 400

        updatedAt = getTimestamp(datetime.now())

        data['updated_at'] = updatedAt

        q = {"_id": ObjectId(data['id'])}

        self.db.room.update(q, {'$set': data})

        self.db.room.find_one(q)

        return data

    def delete(self, id):
        data = request.get_json()

        if data['id'] is None:
            data = {"response": "ERROR"}
            return jsonify(data), 400

        self.db.room.remove({"_id": ObjectId(id)})
        return {}, 200
