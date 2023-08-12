import certifi
import secrets
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from datetime import datetime



# Create a new client and connect to the server
client = MongoClient(secrets.connection_string, tlsCAFile=certifi.where())
db = client["playlify"]
col = db["users"]


# col.create_index("createdAt", expireAfterSeconds=3600)


def get_by_object_id(object_id: str):
    return col.find_one({"_id": ObjectId(object_id)})


def get_by_user_id(user_id: str):
    res = col.find_one({"user_id": user_id})
    return res["data"]


def write_to_db(user_id: str, data: dict):
    res = col.insert_one({"user_id": user_id, "createdAt": datetime.utcnow(), "data": data})
    return res.inserted_id


def has_data_for_user(user_id: str):
    return col.count_documents({'user_id': user_id}, limit=1) != 0


def reset_ttl_for_user(user_id: str):
    col.update_one(
        {'user_id': user_id},
        {'$set': {'createdAt': datetime.utcnow()}}
    )
