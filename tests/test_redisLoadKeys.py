import unittest
from unittest.mock import patch, MagicMock
from gpt_redis.redisLoadKeys import RedisLoadKeys

class TestRedisLoadKeys(unittest.TestCase):

    @patch('gpt_redis.redisLoadKeys.load_event_keys')
    @patch('gpt_redis.redisLoadKeys.RedisHash')
    def test_RedisLoadKeys(self, MockRedisHash, mock_load_event_keys):
        # Setup the return value of load_event_keys
        mock_load_event_keys.return_value = {
            "key": "GPT_KEYS",
            "value": {
                "CALENDAR_EVENT": {"value": "CALENDAR_EVENT"},
                "SMS_EVENT": {"value": "SMS_EVENT"},
                "EMAIL_EVENT": {"value": "EMAIL_EVENT"}
            }
        }

        # Setup the RedisHash mock
        mock_redis_hash_instance = MagicMock()
        MockRedisHash.return_value = mock_redis_hash_instance

        # Call the RedisLoadKeys function
        RedisLoadKeys()

        # Check that RedisHash was called with the correct key
        MockRedisHash.assert_called_once_with(key='GPT_KEYS')

        # Check that the add method was called with the correct values
        mock_redis_hash_instance.add.assert_any_call('CALENDAR_EVENT', {'value': 'CALENDAR_EVENT'})
        mock_redis_hash_instance.add.assert_any_call('SMS_EVENT', {'value': 'SMS_EVENT'})
        mock_redis_hash_instance.add.assert_any_call('EMAIL_EVENT', {'value': 'EMAIL_EVENT'})

if __name__ == '__main__':
    unittest.main()
