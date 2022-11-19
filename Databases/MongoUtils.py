import pymongo


def get_database():

    CONNECTION_STRING = "mongodb://localhost:27017/PopulationRegistry"

    client = pymongo.MongoClient('localhost', 27017)
    db = client['PopulationRegistry']
    person_collection = db['personstemp']
    return person_collection

def insert_document(collection, data):
    return collection.insert_one(data).inserted_id