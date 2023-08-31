import os
import json
from .redisHash import RedisHash
from dotenv import load_dotenv

# Load the .env file. By default, it looks for a file called .env in the same directory as the script.
# If your .env file is located elsewhere, pass the path to load_dotenv.
load_dotenv()

key = os.getenv("REDIS_KEY")
symbol = "ALL"
keys = RedisHash(key)
values = keys.get_all()
cleaned = {}
for key, value in values.items():
    my_dict = json.loads(value)
    first_value = next(iter(my_dict.values()))
    cleaned[key] = first_value

PUBSUB_KEYS = cleaned
