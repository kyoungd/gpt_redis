import time
import threading
import redis
import json
import os
from .iRedisConnction import IRedisAccess

class RedisAccess(IRedisAccess):
    """
    A utility class to establish a connection with a Redis server
    """

    @staticmethod
    def create_connection(r=None, host='127.0.0.1', port=6379, db=0) -> redis.StrictRedis:
        """
        Establish a connection to a Redis server.

        Args:
            r (redis.StrictRedis, optional): A pre-existing Redis connection.
            host (str, optional): The host address of the Redis server.
            port (int, optional): The port number of the Redis server.
            db (int, optional): The database number to connect to on the Redis server.
        
        Returns:
            redis.StrictRedis: The Redis connection.
        """

        if r is None:
            try:
                return redis.StrictRedis(host=host, port=port, db=db)
            except redis.ConnectionError as e:
                # Handle connection error appropriately
                print(f"Could not establish connection: {e}")
                return None
        elif isinstance(r, redis.StrictRedis):
            return r
        else:
            raise ValueError("The 'r' argument must be an instance of redis.StrictRedis or None.")

class DictObj:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, DictObj(value))
            else:
                setattr(self, key, value)

class SetInterval:
    def __init__(self, interval:int, action:callable):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def GetColumn(matrix, i):
    return [row[i] for row in matrix]

def GetRedisEventKeys() -> DictObj:
    file_path = os.path.join(os.path.dirname(__file__), "event_keys.json")
    print(file_path)
    with open(file_path, 'r') as f:
        return DictObj(json.loads(f.read()))

if __name__ == "__main__":
    pass
