def test_set_command(redis_client):
    key = "test_key"
    value = "test_value"
    assert redis_client.set(key, value)
    assert redis_client.get(key).decode('utf-8') == value
    value2 = "test_value2"
    assert redis_client.set(key, value2)
    assert redis_client.get(key).decode('utf-8') == value2


def test_get_command(redis_client):
    key = "test_key"
    value = "test_value"
    redis_client.set(key, value)
    assert redis_client.get(key).decode('utf-8') == value
