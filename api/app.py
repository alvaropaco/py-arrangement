# -*- coding: utf-8 -*-
import sys

from flask import Flask, jsonify, url_for, redirect, request, Blueprint
from flask_restful import Api, Resource
from urllib import quote_plus, quote

from resources.arrange import Arrange
from resources.room import Room
from common.logger import Logger
from common.mongoDB import MongoDb


def routes(api, db):
    api.add_resource(Index, "/v1", endpoint="index")
    api.add_resource(Arrange, "/v1/arrange", "/v1/arrange/<string:id>",
                     endpoint="arrange", resource_class_kwargs={'db': db})
    api.add_resource(Room, "/v1/room", "/v1/room/<string:id>", endpoint="room",
                     resource_class_kwargs={'db': db})


def main(host, port, debug):
    
    # app = application(host, port, debug)
    #Logger(app)
    app.run(host, port, debug)
    
class Index(Resource):
    def get(self):
        return {"response": "health"}

# initialization of Flask Application
app = Flask(__name__)
app.register_blueprint(Blueprint('api', __name__))
mongo = MongoDb(app)
db = mongo.getDb()
routes(Api(app), db)

if __name__ == "__main__":
    main(sys.argv[3:])
