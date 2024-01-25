import threading
from typing import Any
import pickle


class RedisDB:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        # singleton implementation
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, snapshot_filename: str, data: dict | None = None):
        self._snapshot_filename = snapshot_filename
        self._data = data or {}

    @classmethod
    def from_file(cls, snapshot_filename: str) -> "RedisDB":
        return cls(
            snapshot_filename=snapshot_filename,
            data=cls.load_snapshot(snapshot_filename),
        )

    @staticmethod
    def load_snapshot(snapshot_filename: str) -> dict:
        try:
            with open(snapshot_filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def dump_data(self) -> None:
        with open(self._snapshot_filename, "wb") as file:
            pickle.dump(self._data, file)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, item: str):
        return self._data[item]

    def set(self, key: Any, value: Any) -> None:
        self._data[key] = value

    def get(self, key: Any, default: Any | None = None) -> Any:
        return self._data.get(key, default)

    def delete(self, key: Any) -> None:
        del self._data[key]


REDIS_DB = RedisDB.from_file("redis_snapshot.pkl")
