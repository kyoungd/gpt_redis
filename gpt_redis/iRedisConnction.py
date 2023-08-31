from abc import ABC, abstractmethod
import redis

class IRedisAccess(ABC):

    @staticmethod
    @abstractmethod
    def create_connection(r=None, host='127.0.0.1', port=6379, db=0) -> redis.StrictRedis:
        pass
