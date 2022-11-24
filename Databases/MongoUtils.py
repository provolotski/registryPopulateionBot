import bson
import pymongo
import Util.config as config
import Util.log as log
from Databases import RedisUtils
from bson import ObjectId


def get_database():
    client = pymongo.MongoClient(config.MONGO_HOST, int(config.MONGO_PORT))
    db = client[config.MONGO_DATABASE]
    person_collection = db[config.MONGO_COLLECTION]
    return person_collection


def insert_document(collection, data):
    return collection.insert_one(data).inserted_id


def check_relative(level):
    collection = get_database()
    log.logger.debug(f' Mongo connected ')
    log.logger.info(f'работаем по уровню {level}')
    redis = RedisUtils.connect()
    query = {'Family.' + str(level) + '.applic': {"$exists": "true"}}
    mongo_filter = {'Family': 1}
    item_details = collection.find(query, mongo_filter)
    log.logger.debug(f' query executed ')
    i = 0
    j = 0
    for item in item_details:
        i +=1
        item_value = item["Family"]
        value = redis.get(item_value[level]["applic"])
        if value is not None:
            j += 1
            item_value[level]["RelativeID"] = bson.ObjectId(value.decode("utf-8"))
            del item_value[level]["applic"]
            doc = collection.find_one_and_update(
                {"_id":ObjectId(item["_id"])},
                {"$set":
                     {'Family':item_value}
                }
            )
    print(f'count of rows {i} updated rows {j}')
