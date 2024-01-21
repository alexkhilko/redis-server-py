from commands.commands import PingCommand, EchoCommand, GetCommand, SetCommand, ClientCommand, CommandCommand, ExistsCommand, DeleteCommand, IncrCommand, IncrByCommand, DecrCommand, DecrByCommand
from base.exceptions import UnknownCommandException
from commands.base import RedisCommand
    

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
    }
    command_cls = command_map.get(command.upper())
    if not command_cls:
        raise UnknownCommandException(f"ERR Unsupported command `{command}`")
    return command_cls
