import pytest

from base.exceptions import InvalidCommandSyntaxError
from commands import RedisCommand


class TestRedisCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ("key", "value")
    POSSIBLE_OPTIONS = ("foo", "bar")

    def execute(self) -> str:
        self._parse_arguments()
        return self._attributes


@pytest.mark.parametrize(
    "arguments, expected",
    [
        (["test_key", "test_value"], {"key": "test_key", "value": "test_value"}),
        (
            ["test_key", "test_value", "foo", 10],
            {"key": "test_key", "value": "test_value", "foo": 10},
        ),
        (
            ["test_key", "test_value", "foo", 10, "bar", "20"],
            {"key": "test_key", "value": "test_value", "foo": 10, "bar": "20"},
        ),
    ],
)
def test_parse_attributes(arguments, expected):
    command = TestRedisCommand(arguments)
    assert command.execute() == expected


def test_invalid_number_of_arguments():
    command = TestRedisCommand(["test_key"])
    with pytest.raises(InvalidCommandSyntaxError) as exc:
        command.execute()
    assert "ERR wrong number of arguments for command" in str(exc.value)


def test_syntax_error():
    command = TestRedisCommand(("test_key", "test_value", "foo"))
    with pytest.raises(InvalidCommandSyntaxError) as exc:
        command.execute()
    assert "ERR syntax error" in str(exc.value)


def test_invalid_option():
    command = TestRedisCommand(("test_key", "test_value", "fofo", 10))
    with pytest.raises(InvalidCommandSyntaxError) as exc:
        command.execute()
    assert "ERR invalid option: fofo" in str(exc.value)
