import logging
import json
import redis
from typing import Callable, Optional
from .redisUtil import RedisAccess
from .iRedisHash import IRedisHash

class RedisHash(IRedisHash):

    def __init__(self, key: str, r: Optional[redis.StrictRedis]=None, callback: Optional[Callable[[str, dict], None]]=None):
        self.redis = RedisAccess.create_connection(r) if r is None else r
        self.callback = callback
        self._key = key

    @property
    def key(self):
        """Return the hash key."""
        return self._key

    # def get_all(self):
    #     """Return all hash fields/values for the given key."""
    #     return self.redis.hgetall(self.key)

    def get_all(self):
        """Return all hash fields/values for the given key."""
        raw_data = self.redis.hgetall(self.key)
        decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in raw_data.items()}
        return decoded_data

    def get_all_symbols(self):
        """Return all fields for the key."""
        arrayOfByteArray = self.redis.hkeys(self.key)
        return [item.decode('utf-8') for item in arrayOfByteArray]

    def add(self, symbol, jsondata):
        """Add a new field/value pair to the hash."""
        data = json.dumps(jsondata)
        self.redis.hset(self.key, symbol, data)
        if self.callback is not None:
            self.callback(symbol, jsondata)

    def delete(self, symbol):
        """Delete a field/value pair from the hash key."""
        self.redis.hdel(self.key, symbol)

    def get(self, symbol):
        """Return value from redis hash key field."""
        data = self.redis.hget(self.key, symbol)
        if data is None:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON data: {e}")
            return None

    def is_symbol_exist(self, symbol):
        """Check if a field exists in the hash key."""
        return self.redis.hexists(self.key, symbol)

    def delete_all(self):
        """Delete all fields/values from the hash key."""
        if self.redis.hlen(self.key) > 0:
            self.redis.delete(self.key)
