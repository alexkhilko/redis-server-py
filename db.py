import threading
from typing import Any


class RedisDB:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._data = {}
            return cls._instance
        
    def __contains__(self, key) -> bool:
        return key in self._data
    
    def __getitem__(self, index):
        return self._data[index]
    
    def set(self, key, value) -> None:
        self._data[key] = value

    def get(self, key, default=None) -> Any:
        return self._data.get(key, default)

    def delete(self, key) -> None:
        del self._data[key]
    


REDIS_DB = RedisDB()
