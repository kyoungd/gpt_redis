import unittest
from unittest.mock import create_autospec, MagicMock
from redis import StrictRedis
from gpt_redis.iRedisHash import IRedisHash
from gpt_redis.redisHash import RedisHash

class TestRedisHash(unittest.TestCase):

    def setUp(self):
        self.redis_mock = create_autospec(StrictRedis)
        self.redis_hash: IRedisHash = RedisHash('test_key', r=self.redis_mock)

    def test_key_property(self):
        self.assertEqual(self.redis_hash.key, 'test_key')

    def test_add(self):
        self.redis_hash.add('field', {'data': 'value'})
        self.redis_mock.hset.assert_called_once_with('test_key', 'field', '{"data": "value"}')

    def test_delete(self):
        self.redis_hash.delete('field')
        self.redis_mock.hdel.assert_called_once_with('test_key', 'field')

    def test_get(self):
        self.redis_mock.hget.return_value = '{"data": "value"}'
        result = self.redis_hash.get('field')
        self.redis_mock.hget.assert_called_once_with('test_key', 'field')
        self.assertEqual(result, {'data': 'value'})

    def test_is_symbol_exist(self):
        self.redis_hash.is_symbol_exist('field')
        self.redis_mock.hexists.assert_called_once_with('test_key', 'field')

    def test_delete_all(self):
        self.redis_mock.hlen.return_value = 1
        self.redis_hash.delete_all()
        self.redis_mock.delete.assert_called_once_with('test_key')

if __name__ == '__main__':
    unittest.main()
