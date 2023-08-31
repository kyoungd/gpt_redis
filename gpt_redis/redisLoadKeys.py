# read event_keys.json
import json
import os
from .redisHash import RedisHash

def load_event_keys() -> dict:
    file_path = "./event_keys.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    else:
        return {}

def RedisLoadKeys() -> dict:
    keys = load_event_keys()
    hash = RedisHash(key = keys['key'])
    values:dict = keys['value']
    # get key and vlue from values
    for key, value in values.items():
        hash.add(key, value)


