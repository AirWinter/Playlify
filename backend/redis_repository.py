import redis
from backend import secrets

r = redis.Redis(
    host=secrets.db_host,
    port=secrets.db_port,
    password=secrets.db_password,
    decode_responses=True)


def get_from_db(key):
    res = r.json().get(key)
    return res


def has_key(key):
    res = r.exists(key)
    return res


def write_to_db(key, value):
    r.json().set(key, '$', value)
    r.expire(key, 3600)
