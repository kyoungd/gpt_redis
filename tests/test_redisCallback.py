import unittest
import time
from redis import StrictRedis
from json import dumps
from gpt_redis.redisPubsub import RedisSubscriber, RedisPublisher, RedisPublishReturn
from gpt_redis.redisUtil import GetRedisEventKeys, DictObj

class TestRedisPublishReturnLive(unittest.TestCase):

    def test_event_keys(self):
        keys = GetRedisEventKeys()
        self.assertIsNotNone(keys)
        self.assertIsInstance(keys, DictObj)

    def test_pubsub(self):
        keys = GetRedisEventKeys()
        key = keys.events.test_event
        data = {
            "data": {"message": "Hello, world!"}
        }

        isCalled = False

        def sub_callback(data: dict):
            nonlocal isCalled
            isCalled = True
            self.assertTrue(isCalled)
            return data
        
        def run_subscriber(channel: str):
            subscription_name = keys.subscriptions.test_event
            RedisSubscriber.Running(subscription_name, [channel], callback=sub_callback)

        run_subscriber(channel=key)
        RedisPublisher.Running(channel=key, data=data)

    def test_publish_return(self):
        keys = GetRedisEventKeys()
        key = keys.events.test_event_return

        data = {
            "data": {"message": "Hello, world!"}
        }

        def subscription_callback(data: dict):
            return data

        block = RedisPublishReturn(keys.subscriptions.test_event_return, channel=key, data=data, sub_callback=subscription_callback)
        self.assertIsNotNone(block)
        self.assertIn('return_channel', block)
        self.assertIn('message', block)


if __name__ == '__main__':
    unittest.main()
