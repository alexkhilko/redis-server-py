import pytest
from resp.parsers import deserialize, serialize


@pytest.mark.parametrize(
    "resp_string, expected",
    [
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
        ("*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n", ["echo", "hello world"]),
    ],
)
def test_deserialize(resp_string, expected):
    assert deserialize(resp_string) == expected


@pytest.mark.parametrize(
    "resp_string, expected, use_bulk",
    [
        ("OK", "+OK\r\n", False),
        ("", "$0\r\n\r\n", True),
        (None, "$-1\r\n", True),
        (1000, ":1000\r\n", True),
        (-1000, ":-1000\r\n", True),
        ("foobar", "$6\r\nfoobar\r\n", True),
        ([], "*0\r\n", True),
        (["hello", None, "world"], "*3\r\n$5\r\nhello\r\n$-1\r\n$5\r\nworld\r\n", True),
        (["foo", "bar"], "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n", True),
        ([1, 2, 3], "*3\r\n:1\r\n:2\r\n:3\r\n", True),
        (["echo", "hello world"], "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n", True),
    ],
)
def test_serialize(resp_string, expected, use_bulk):
    assert serialize(resp_string, use_bulk) == expected
