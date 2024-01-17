import time
import pytest

value = "test_value"


@pytest.fixture
def key():
    return f"test_{time.time_ns()}"


def test_set_command(key, redis_client):
    assert redis_client.set(key, value)
    assert redis_client.get(key).decode('utf-8') == value
    value2 = "test_value2"
    assert redis_client.set(key, value2)
    assert redis_client.get(key).decode('utf-8') == value2


def test_get_command(key, redis_client):
    redis_client.set(key, value)
    assert redis_client.get(key).decode('utf-8') == value
    

def test_set_with_ex(key, redis_client):
    redis_client.set(key, value, ex=1)
    assert redis_client.get(key).decode('utf-8') == value
    time.sleep(2)
    assert redis_client.get(key) is None


def test_set_with_px(key, redis_client):
    redis_client.set(key, value, px=1000)
    assert redis_client.get(key).decode('utf-8') == value
    time.sleep(0.6)
    assert redis_client.get(key).decode('utf-8') == value
    time.sleep(2)
    assert redis_client.get(key) is None


def test_set_with_exat(key, redis_client):
    redis_client.set(key, value, exat=int(time.time()) + 1)
    assert redis_client.get(key).decode('utf-8') == value
    time.sleep(2)
    assert redis_client.get(key) is None


def test_set_with_pxat(key, redis_client):
    redis_client.set(key, value, pxat=int(time.time() * 1000) + 1000)
    assert redis_client.get(key).decode('utf-8') == value
    time.sleep(2)
    assert redis_client.get(key) is None
