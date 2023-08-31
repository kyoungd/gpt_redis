import unittest
from unittest.mock import patch, MagicMock
import json
from gpt_redis.redisDataPackage import RedisDataPackage
from gpt_redis.redisUtil import GetRedisEventKeys, DictObj

class TestRedisDataPackage(unittest.TestCase):

    def setUp(self):
        self.keys:DictObj = GetRedisEventKeys()

    def test_RedisAddEvent(self):
        data = {
            "template": "test_template",
            "start_time": "2023-09-01T14:30:00-04:00",
            "description": "test description"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.calendar_add_event, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 30)

    def test_RedisAddEvent_RaiseError(self):
        data = {
            "template": "test_template",
            "start_time": "2023-09-01T14:30:00-04:00"
        }
        with self.assertRaises(KeyError):
            RedisDataPackage.Encode(event_key=self.keys.events.calendar_add_event, data=data)

    def test_RedisEditEvent(self):
        data = {
            "template": "test_template",
            "start_time": "2023-09-01T14:30:00-04:00",
            "description": "test description"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.calendar_edit_event, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 30)

    def test_RedisCancelEvent(self):
        data = {
            "template": "test_template",
            "start_time": "2023-09-01T14:30:00-04:00"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.calendar_cancel_event, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 30)

    def test_RedisRefreshCalendar(self):
        data = {
            "template": "test_template"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.calendar_refresh_calendar, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 10)

    def test_RedisGetAvailableAppointments(self):
        data = {
            "template": "test_template"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.calendar_get_available_appointments, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 10)

    def test_RedisSendSMS(self):
        data = {
            "phone_number": "5555555555",
            "message": "test message"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.sms_send, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 10)

    def test_RedisSendEmail(self):
        data = {
            "email": "test@test.com",
            "subject": "test subject",
            "message": "test message"
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.email_send, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 10)


    def test_RedisTest(self):
        data = {
            "data": {"message": "Hello, world!"}
        }
        result = RedisDataPackage.Encode(event_key= self.keys.events.test_event, data=data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 10)

    def test_RedisDecode(self):
        data = {
            "template": "test_template",
            "start_time": "2023-09-01T14:30:00-04:00",
            "description": "test description"
        }
        block = json.dumps(data)
        result = RedisDataPackage.Decode(event_key= self.keys.events.calendar_add_event, data=block)
        self.assertIsNotNone(result)
        self.assertIn("template", result)
        self.assertIn("start_time", result)
        self.assertIn("description", result)

if __name__ == '__main__':
    unittest.main()
