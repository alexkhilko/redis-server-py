import pytest
from resp.parsers import serialize
from base.parsers import RespParser


@pytest.mark.parametrize(
    "resp_string, expected",
    [
        (b"+OK\r\n", "OK"),
        (b"$0\r\n\r\n+OK\r\n", ""),
        (b"$-1\r\n", None),
        (b"-Error message\r\n", "Error message"),
        (b":1000\r\n", 1000),
        (b":-1000\r\n", -1000),
        (b"$6\r\nfoobar\r\n", "foobar"),
        (b"*-1\r\n", None),
        (b"*3\r\n$5\r\nhello\r\n$-1\r\n$5\r\nworld\r\n", ["hello", None, "world"]),
        (b"*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n", ["foo", "bar"]),
        (b"*3\r\n:1\r\n:2\r\n:3\r\n", [1, 2, 3]),
        (b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n", ["echo", "hello world"]),
    ],
)
def test_resp_parser(resp_string, expected):
    parser = RespParser(data=resp_string)
    assert parser.parse() == expected


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
