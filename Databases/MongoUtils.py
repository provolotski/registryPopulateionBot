import pymongo
import Util.config as config


def get_database():

    client = pymongo.MongoClient(config.mongo_host, config.mongo_port)
    db = client[config.mongo_database]
    person_collection = db[config.mongo_collection]
    return person_collection


def insert_document(collection, data):
    return collection.insert_one(data).inserted_id
