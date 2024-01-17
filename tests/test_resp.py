import pytest
from base.parsers import RespParser, RespSerializer
from base.exceptions import RespProtocolError, RespParsingError


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
def test_parser(resp_string, expected):
    parser = RespParser(data=resp_string)
    assert parser.parse() == expected


def test_parse_error():
    with pytest.raises(RespParsingError):
        parser = RespParser(data=b":foo\r\n")
        parser.parse()

    
def test_parse_protocol_error():
    with pytest.raises(RespProtocolError):
        parser = RespParser(data=b">foo")
        parser.parse()


@pytest.mark.parametrize(
    "value, expected, use_bulk",
    [
        ("OK", b"+OK\r\n", False),
        ("", b"$0\r\n\r\n", True),
        (None, b"$-1\r\n", True),
        (1000, b":1000\r\n", True),
        (-1000, b":-1000\r\n", True),
        ("foobar", b"$6\r\nfoobar\r\n", True),
        ([], b"*0\r\n", True),
        (["hello", None, "world"], b"*3\r\n$5\r\nhello\r\n$-1\r\n$5\r\nworld\r\n", True),
        (["foo", "bar"], b"*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n", True),
        ([1, 2, 3], b"*3\r\n:1\r\n:2\r\n:3\r\n", True),
        (["echo", "hello world"], b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n", True),
    ],
)
def test_serialize(value, expected, use_bulk):
    serializer = RespSerializer()
    assert serializer.serialize(data=value, use_bulk=use_bulk) == expected


def test_serialize_error():
    with pytest.raises(RespProtocolError):
        serializer = RespSerializer()
        serializer.serialize(data=object())