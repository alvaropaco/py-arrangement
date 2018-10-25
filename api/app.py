# -*- coding: utf-8 -*-
from flask import Flask, jsonify, url_for, redirect, request, Blueprint
from flask_pymongo import PyMongo, MongoClient
from flask_restful import Api, Resource
from urllib import quote_plus, quote

from resources.arrange import Arrange

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
app.register_blueprint(api_bp)

uri = "mongodb://%s:%s@%s:%d/desafioluiza" % (
    quote_plus("alvaropaco"), quote_plus("k8xrmmTAGh9VCN3"), 
    quote_plus("cluster0-shard-00-00-h3iwf.mongodb.net"), 27017)

app.config["MONGO_URI"] = uri
app.config["MONGO_DBNAME"] = "desafioluiza"

mongo = PyMongo(app)
client = MongoClient(uri)
db = client.desafioluiza


class Index(Resource):
    def get(self):
        return {"response": "Hello World"}

api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Arrange, "/v1", endpoint="arrange", 
    resource_class_kwargs={ 'db': db })
# api.add_resource(Arrange, "/v1/<string:id>", endpoint="id")
# api.add_resource(Arrange, "/v1/emotion/<string:emotion>", endpoint="emotion")
# api.add_resource(Arrange, "/v1/range/<string:range>", endpoint="range")

if __name__ == "__main__":
    print(db)
    app.run(debug=True)