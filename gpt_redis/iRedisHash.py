from abc import ABC, abstractmethod

class IRedisHash(ABC):

    @property
    @abstractmethod
    def key(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_all_symbols(self):
        pass

    @abstractmethod
    def add(self, symbol, jsondata):
        pass

    @abstractmethod
    def delete(self, symbol):
        pass

    @abstractmethod
    def get(self, symbol):
        pass

    @abstractmethod
    def is_symbol_exist(self, symbol):
        pass

    @abstractmethod
    def delete_all(self):
        pass
    