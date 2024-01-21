import time
import pytest
from redis.exceptions import ResponseError

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


@pytest.mark.parametrize("keys,expected_count", [
    (("key",), 1),
    (("key", "key",), 2),
    (("key", "key2",), 2),
    (("key", "key4",), 1),
])
def test_exists(keys, expected_count, redis_client):
    redis_client.set("key", 1)
    redis_client.set("key2", 1)
    assert redis_client.exists(*keys) == expected_count


def test_exists_with_expire(key, redis_client):
    redis_client.set(key, 1, px=500)
    assert redis_client.exists(key) == 1
    time.sleep(1)
    assert redis_client.exists(key) == 0


def test_delete(redis_client):
    redis_client.set("foo", 1)
    redis_client.set("bar", 1)
    assert redis_client.delete("foo", "bar", "sadfsafdsa") == 2
    assert redis_client.delete("foo") == 0


def test_increment(key, redis_client):
    redis_client.set(key, 3)
    assert redis_client.incr(key) == 4
    assert redis_client.incr(key) == 5


def test_increment_new_key(key, redis_client):
    assert redis_client.incr(key) == 1


def test_increment_with_expire(key, redis_client):
    redis_client.set(key, 3, px=500)
    time.sleep(1)
    assert redis_client.incr(key) == 1


def test_increment_wrong_value_type(key, redis_client):
    redis_client.set(key, "bar")
    with pytest.raises(ResponseError) as exc:
        redis_client.incr(key)
    assert "ERR value is not an integer or out of range" in str(exc.value)


def test_decrement(key, redis_client):
    redis_client.set(key, 3)
    assert redis_client.decr(key) == 2
    assert redis_client.decr(key) == 1


def test_decrement_new_key(key, redis_client):
    assert redis_client.decr(key) == -1


def test_decrement_with_expire(key, redis_client):
    redis_client.set(key, 3, px=100)
    time.sleep(1)
    assert redis_client.decr(key) == -1


def test_decrement_wrong_value_type(key, redis_client):
    redis_client.set(key, "bar")
    with pytest.raises(ResponseError) as exc:
        redis_client.decr(key)
    assert "ERR value is not an integer or out of range" in str(exc.value)


def test_lpush(key, redis_client):
    assert redis_client.lpush(key, 1) == 1
    assert redis_client.lpush(key, 2, 3) == 3


def test_lpush_wrong_value_type(key, redis_client):
    redis_client.set(key, 1)
    with pytest.raises(ResponseError) as exc:
        redis_client.lpush(key, 1)
    assert "WRONGTYPE Operation against a key holding the wrong kind of value" in str(exc.value)


def test_rpush(key, redis_client):
    assert redis_client.rpush(key, 1) == 1
    assert redis_client.rpush(key, 2, 3) == 3


def test_rpush_wrong_value_type(key, redis_client):
    redis_client.set(key, 1)
    with pytest.raises(ResponseError) as exc:
        redis_client.rpush(key, 1)
    assert "WRONGTYPE Operation against a key holding the wrong kind of value" in str(exc.value)
