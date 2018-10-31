from os import environ
from flask_pymongo import PyMongo, MongoClient

mongo_host = environ['MONGO_HOST']
mongo_user = environ['MONGO_USER']
mongo_pass = environ['MONGO_PASS']
mongo_port = environ['MONGO_PORT']
mongo_dB = environ['MONGO_DB']


class MongoDb:
    def __init__(self, app):
        uri = ("mongodb://{user}:{password}@{host}:{port}/{db}?ssl=false").format(
            user=mongo_user, password=mongo_pass,
            host=mongo_host, port=mongo_port, db=mongo_dB)
        
        app.config["MONGO_URI"] = uri
        app.config["MONGO_DBNAME"] = "desafioluiza"

        mongo = PyMongo(app)
        client = MongoClient(uri)

        self.db = client.desafioluiza
    
    def getDb(self):
        return self.db
