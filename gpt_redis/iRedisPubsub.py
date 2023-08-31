from abc import ABC, abstractmethod
from typing import Optional, Callable
import threading
import redis

class IRedisSubscriber(ABC, threading.Thread):

    @abstractmethod
    def work(self, package: dict):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def wait_until_ready(self):
        pass

    @staticmethod
    @abstractmethod
    def Running(subscription_name, channels: list[str] | str, callback: Optional[Callable[[dict], None]]=None, isRunOnlyOnce: bool=False):
        pass


class IRedisPublisher:

    @abstractmethod
    def publish(self, data: dict):
        pass

    @abstractmethod
    def stop_subscriber(self):
        pass
 
    @staticmethod
    @abstractmethod
    def Running(channel: str, data: dict, r: Optional[redis.StrictRedis]=None):
        pass

