import certifi
from backend import secrets
from pymongo.mongo_client import MongoClient
from datetime import datetime

# Create a new client and connect to the server
client = MongoClient(secrets.connection_string, tlsCAFile=certifi.where())
db = client["playlify"]
col = db["users"]


# col.create_index("createdAt", expireAfterSeconds=3600)

def get_by_user_id(user_id: str):
    res = col.find_one({"_id": user_id})
    return res


def write_to_db(user_id: str, songs: dict, artist_options: dict, genre_options: dict):
    res = col.insert_one(
        {"_id": user_id, "createdAt": datetime.utcnow(), "songs": songs, "artist_options": artist_options,
         "genre_options": genre_options})
    return res.inserted_id


def has_data_for_user(user_id: str):
    return col.count_documents({'_id': user_id}, limit=1) != 0


def reset_ttl_for_user(user_id: str):
    col.update_one(
        {'_id': user_id},
        {'$set': {'createdAt': datetime.utcnow()}}
    )
