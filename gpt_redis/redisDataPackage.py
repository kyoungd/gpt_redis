from dataclasses import dataclass
from typing import Any
from .redisUtil import GetRedisEventKeys, DictObj
import json

@dataclass
class PackageEncode():
    def __post_init__(self):
        self.keys:DictObj = GetRedisEventKeys()
        self.data: dict = {}

    def TEST_EVENT(self, data: Any) -> dict:
        package = {
            'message': data['data']['message']
        }
        return package

    def TEST_EVENT_RETURN(self, data: Any) -> dict:
        package = {
            'return_channel': data['return_channel'],
            'message': data['data']['message']
        }
        return package

    def CALENDAR_ADD_EVENT(self, data: Any) -> dict:
        package = {
            'template': data['template'],
            'start_time': data['start_time'],
            'description': data['description']
        }
        return package

    def CALENDAR_EDIT_EVENT(self, data: Any) -> dict:
        return self.CALENDAR_ADD_EVENT(data)
    
    def CALENDAR_CANCEL_EVENT(self, data: Any) -> dict:
        package = {
            'template': data['template'],
            'start_time': data['start_time'],
        }
        return package

    def CALENDAR_REFRESH_CALENDAR(self, data: Any) -> dict:
        package = {
            'template': data['template']
        }
        if 'projected_days' in data:
            package['projected_days'] = data['projected_days']
        return package
    
    def CALENDAR_GET_AVAILABLE_APPOINTMENTS(self, data: Any) -> dict:
        package = self.CALENDAR_REFRESH_CALENDAR(data)
        return package

    def SMS_SEND(self, data: Any)-> dict:
        package = {
            'phone_number': data['phone_number'],
            'message': data['message']
        }
        return package
    
    def EMAIL_SEND(self, data: Any) -> dict:
        package = {
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message']
        }
        return package

    @staticmethod
    def run(event_key: str, data: Any) -> str:
        # if event_key starts with "RETURN-":
        if event_key.startswith("RETURN-"):
            return json.dumps(data)
        encode = PackageEncode()
        method: Any = getattr(encode, event_key)
        result: dict = method(data)
        return json.dumps(result)

@dataclass
class PackageDecode():
    def __post_init__(self):
        self.keys:DictObj = GetRedisEventKeys()

    @staticmethod
    def run(event_key: str, data: str) -> dict:
        package = json.loads(data)
        return package


@dataclass
class RedisDataPackage():

    @staticmethod
    def Encode(event_key, data: Any) -> Any:
        return PackageEncode.run(event_key, data)

    @staticmethod
    def Decode(event_key, data: str) -> dict:
        return PackageDecode.run(event_key, data)

