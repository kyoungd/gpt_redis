import threading
import json
import redis
import logging
from typing import Callable, Optional, List, TYPE_CHECKING
import threading
from .redisUtil import RedisAccess
from .iRedisPubsub import IRedisSubscriber, IRedisPublisher
from .redisDataPackage import RedisDataPackage
import uuid

if TYPE_CHECKING:
    from .redisPubsub import RedisSubscriber  # Assuming RedisSubscriber is in 'your_module_name.py'


class SubscriptionRegistry:
    subscriptions: dict = {}
    # Creating a lock for thread safety
    lock = threading.Lock()

    @classmethod
    def register(cls, subscription_name: str, channels: List[str] | str, subscriber: Optional['RedisSubscriber']=None):
        if not subscriber:
            raise ValueError("Subscriber is required for registration!")

        with cls.lock:
            for channel in channels if isinstance(channels, list) else [channels]:
                if channel in cls.subscriptions:
                    if subscription_name in cls.subscriptions[channel]:
                        cls.subscriptions[channel][subscription_name].unsubscribe()
                        del cls.subscriptions[channel][subscription_name]
            
            for channel in channels if isinstance(channels, list) else [channels]:
                if channel not in cls.subscriptions:
                    cls.subscriptions[channel] = {}
                cls.subscriptions[channel][subscription_name] = subscriber
            
            if not subscriber.is_alive():
                subscriber.start()

    @classmethod
    def unregister(cls, subscription_name: str, channel: str):
        with cls.lock:
            if channel in cls.subscriptions and subscription_name in cls.subscriptions[channel]:
                cls.subscriptions[channel][subscription_name].unsubscribe()
                del cls.subscriptions[channel][subscription_name]

    @classmethod
    def clear_all(cls):
        with cls.lock:
            for channel, subs in cls.subscriptions.items():
                for subscription_name, subscriber in subs.items():
                    subscriber.unsubscribe()
                    del cls.subscriptions[channel][subscription_name]

subscription_registry = SubscriptionRegistry()

class RedisSubscriber(IRedisSubscriber, threading.Thread):
    def __init__(self, subscription_name: str, channels: List[str] | str, r: Optional[redis.StrictRedis]=None, callback: Optional[Callable[[dict], None]]=None, isRunOnlyOnce: bool=False):
        super(RedisSubscriber, self).__init__()
        
        if isinstance(channels, str):
            channels = [channels]
        
        self.subscription_name = subscription_name
        self.channels = channels
        self.redis = RedisAccess.create_connection(r)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.callback = callback
        self.isRunOnlyOnce = isRunOnlyOnce
        self.ready_event = threading.Event()
        
        subscription_registry.register(self.subscription_name, self.channels, self)

    def work(self, package: dict):
        try:
            if self.callback is None:
                print(f"{package['channel']} : {package['data']}")
            else:
                data_json: dict = RedisDataPackage.Decode(event_key=package['channel'], data=package['data'])
                self.callback(data_json)
        except (json.JSONDecodeError, Exception) as e:
            logging.error(f"Failed to process package: {e}")

    def unsubscribe(self):
        self.pubsub.unsubscribe()
        for channel in self.channels:
            subscription_registry.unregister(self.subscription_name, channel)
        self.ready_event.clear()
        print("Unsubscribed and finished.")
    
    def run(self):
        self.ready_event.set()
        for package in self.pubsub.listen():
            if package['type'] != 'message':
                continue
            if package['data'] == "KILL":
                self.unsubscribe()
                break
            self.work(package)
            if self.isRunOnlyOnce:
                self.unsubscribe()
                break

    def wait_until_ready(self):
        self.ready_event.wait()

    @staticmethod
    def Running(subscription_name, channels: List[str] | str, callback: Optional[Callable[[dict], None]]=None, isRunOnlyOnce: bool=False) -> 'RedisSubscriber' :
        for channel in channels if isinstance(channels, list) else [channels]:
            subscription_registry.unregister(subscription_name, channel)
        subscriber = RedisSubscriber(subscription_name, channels, callback=callback, isRunOnlyOnce=isRunOnlyOnce)
        subscriber.wait_until_ready()
        return subscriber


class RedisPublisher(IRedisPublisher):
    def __init__(self, channel: str, r: Optional[redis.StrictRedis]=None):
        self.redis = RedisAccess.create_connection(r)
        self.channel = channel

    def publish(self, data: dict) -> None:
        package = RedisDataPackage.Encode(event_key=self.channel, data=data)
        # package = json.dumps(data)
        self.redis.publish(self.channel, package)

    def stop_subscriber(self):
        self.redis.publish(self.channel, 'KILL')

    @staticmethod
    def Running(channel: str, data: dict, r: Optional[redis.StrictRedis]=None) -> None:
        publisher = RedisPublisher(channel, r)
        publisher.publish(data)

def RedisPublishCallbackFunc(func: Callable[[dict], dict]) -> Callable:
    def wrapper(data: dict) -> None:
        return_channel = data.get('return_channel') # Using get() to avoid KeyError
        result = func(data)
        if isinstance(result, dict) and return_channel:
            RedisPublisher(channel=return_channel).publish(result)
    return wrapper


def RedisPublishCallbackData(data: dict) -> dict:
    data['return_channel'] = data.get('return_channel', 'RETURN-' + str(uuid.uuid4()))
    return data

def RedisPublishReturn(subscription_name: str, channel: str, data: dict, sub_callback: Callable[[dict], dict], r: Optional[redis.StrictRedis]=None) -> None:
    block: dict = None
    oncomplete: threading.Event = threading.Event()

    def publisher_callback(data: dict) -> None:
        nonlocal block
        block = data
        oncomplete.set()
   
    package = RedisPublishCallbackData(data)
    subscription_callback = RedisPublishCallbackFunc(sub_callback)
    return_key = package['return_channel']
    RedisSubscriber.Running(subscription_name, channels=[channel], callback=subscription_callback)
    RedisSubscriber.Running(subscription_name, channels=[return_key], callback=publisher_callback)
    RedisPublisher.Running(channel=channel, data=data)
    oncomplete.wait()
    return block

