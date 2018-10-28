# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, jsonify, url_for, redirect, request, Blueprint
from flask_pymongo import PyMongo, MongoClient
from flask_restful import Api, Resource
from urllib import quote_plus, quote

from resources.arrange import Arrange
from common.logger import Logger

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
app.register_blueprint(api_bp)

mongo_user = os.environ['MONGO_USER']
mongo_pass = os.environ['MONGO_PASS']
mongo_port = os.environ['MONGO_PORT']
mongo_dB   = os.environ['MONGO_DB']
uri = ("mongodb://{user}:{password}@" + 
      "cluster0-shard-00-00-h3iwf.mongodb.net:27017," + 
      "cluster0-shard-00-01-h3iwf.mongodb.net:27017," +
      "cluster0-shard-00-02-h3iwf.mongodb.net:{port}/{db}?"+ 
      "ssl=true&readPreference=secondary&" +
      "replicaSet=Cluster0-shard-0&authSource=admin").format(
          user=mongo_user, password=mongo_pass, 
          port=mongo_port, db=mongo_dB)
app.config["MONGO_URI"] = uri
app.config["MONGO_DBNAME"] = "desafioluiza"

APP_URL = "http://127.0.0.1:8080"

mongo = PyMongo(app)
client = MongoClient(uri)
db = client.desafioluiza

def main(host, port ,debug):
    Logger(app)
    app.run(host, port ,debug)

class Index(Resource):
    def get(self):
        return {"response": "health"}

api = Api(app)
api.add_resource(Index, "/v1", endpoint="index")
api.add_resource(Arrange, "/v1/arrange", endpoint="arrange", 
    resource_class_kwargs={ 'db': db })

if __name__ == "__main__":
    main(sys.argv[3:])