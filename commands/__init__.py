from base.exceptions import UnknownCommandException
from commands.base import RedisCommand
from commands.commands import (ClientCommand, CommandCommand, DecrByCommand,
                               DecrCommand, DeleteCommand, EchoCommand,
                               ExistsCommand, GetCommand, IncrByCommand,
                               IncrCommand, LPushCommand, PingCommand,
                               RPushCommand, SaveCommand, SetCommand)


def get_command_handler(command: str) -> RedisCommand:
    command_map = {
        "PING": PingCommand,
        "ECHO": EchoCommand,
        "GET": GetCommand,
        "SET": SetCommand,
        "CLIENT": ClientCommand,
        "COMMAND": CommandCommand,
        "EXISTS": ExistsCommand,
        "DEL": DeleteCommand,
        "INCRBY": IncrByCommand,
        "INCR": IncrCommand,
        "DECR": DecrCommand,
        "DECRBY": DecrByCommand,
        "LPUSH": LPushCommand,
        "RPUSH": RPushCommand,
        "SAVE": SaveCommand,
    }
    command_cls = command_map.get(command.upper())
    if not command_cls:
        raise UnknownCommandException(f"ERR Unsupported command `{command}`")
    return command_cls
