from db import RedisDB
from collections import deque
import pytest
import os
import pickle
import string
import random


def _get_random_string(length: int = 10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


test_db = RedisDB("foo")


@pytest.fixture
def filename():
    name = f"test_{_get_random_string()}.pkl"
    yield name
    if os.path.exists(name):
        os.remove(name)


def test_store_and_retrieve():
    test_db.set("key", "value")
    assert test_db.get("key") == "value"
    assert test_db["key"] == "value"
    assert test_db.get("key2") is None
    assert test_db.get("key2", "default") == "default"


def test_delete():
    test_db.set("key", "value")
    test_db.delete("key")
    assert "key" not in test_db


def test_save_to_file(filename):
    db = RedisDB(filename)
    db.set("key", "value")
    db.set("queue", deque("foo"))
    db.set("list", ["list"])
    db.dump_data()
    assert os.path.exists(filename)
    with open(filename, "rb") as file:
        data = pickle.load(file)
    assert data == {"key": "value", "queue": deque("foo"), "list": ["list"]}


def test_restore_from_file(filename):
    data = {"key": "value", "queue": deque("foo"), "list": ["list"]}
    with open(filename, "wb") as file:
        pickle.dump(data, file)
    db = RedisDB.from_file(filename)
    assert db._data == data
