import pytest
from resp.parsers import deserialize


@pytest.mark.parametrize("resp_string, expected", [
    ("+OK\r\n", "OK"),
    ("$0\r\n\r\n", ""),
    ("$-1\r\n", None),
    ("-Error message\r\n", "Error message"),
    (":1000\r\n", 1000),
    (":-1000\r\n", -1000),
    ("$6\r\nfoobar\r\n", "foobar"),
    ("*-1\r\n", None),
    ("*3\r\n$5\r\nhello\r\n$-1\r\n$5\r\nworld\r\n", ["hello", None, "world"]),
    ("*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n", ["foo", "bar"]),
    ("*3\r\n:1\r\n:2\r\n:3\r\n", [1, 2, 3]),
])
def test_deserialize(resp_string, expected):
    assert deserialize(resp_string) == expected

