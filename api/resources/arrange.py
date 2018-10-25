from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo, MongoClient
from flask_restful import fields, marshal_with, reqparse, Resource
from urllib import quote_plus

APP_URL = "http://127.0.0.1:5000"

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
    'start_at', dest='endAt',
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
        data = []

        if id:
            tweet_info = mongo.db.tweets.find_one({"id": id}, {"_id": 0})
            if tweet_info:
                return jsonify({"status": "ok", "data": tweet_info})
            else:
                return {"response": "no tweet found for {}".format(id)}

        elif range:
            #YYYYMMDDHHMMSS
            range = range.split('to')
            cursor = mongo.db.tweets.find({"timestamp":{"$gt": int(range[0])}, "timestamp":{"$lt": int(range[1])}}, {"_id": 0}).limit(10)
            for tweet in cursor:
                tweet['url'] = APP_URL + url_for('tweets') + "/" + tweet.get('id')
                data.append(tweet)

            return jsonify({"range": range, "response": data})

        elif emotion:
            cursor = mongo.db.tweets.find({"emotion": emotion}, {"_id": 0}).limit(10)
            for tweet in cursor:
                tweet['url'] = APP_URL + url_for('tweets') + "/" + tweet.get('id')
                data.append(tweet)

            return jsonify({"emotion": emotion, "response": data})

        else:
            cursor = mongo.db.tweets.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for tweet in cursor:
                print(tweet)
                tweet['url'] = APP_URL + url_for('tweets') + "/" + tweet.get('id')
                data.append(tweet)

            return jsonify({"response": data})

    @marshal_with(arrange_fields)
    def post(self):
        data = post_parser.parse_args()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            arrange = self.db.insert(data)
            return arrange
        # else:
        #     id = data.get('id')
        #     if id:
        #         if db.find_one({"id": id}):
        #             return {"response": "already exists."}
        #         else:
        #             db.insert(data)
        #     else:
        #         return {"response": "id number missing"}
        # return redirect(url_for("arrangement"))

    def put(self, id):
        data = request.get_json()
        mongo.db.tweets.update({'id': id}, {'$set': data})
        return redirect(url_for("tweets"))

    def delete(self, id):
        mongo.db.tweets.remove({'id': id})
        return redirect(url_for("tweets"))
