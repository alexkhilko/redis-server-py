import time
from commands.base import RedisCommand
from base.exceptions import UnknownCommandException


class PingCommand(RedisCommand):
    def execute(self) -> str:
        return "PONG"


class EchoCommand(RedisCommand):
    def execute(self) -> str:
        return self._arguments


class ClientCommand(RedisCommand):
    def execute(self) -> str:
        return ["OK"]


class CommandCommand(RedisCommand):
    def execute(self) -> str:
        return ["OK"]
    

redis_db = {}

def _get_current_time_in_ms() -> int:
    return int(time.time()) * 1000


class GetCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = {"key"}

    def execute(self) -> str:
        self._parse_arguments()
        key = self.get("key")
        value, expires = redis_db.get(key, [None, None])
        if expires is not None and expires < _get_current_time_in_ms():
            del redis_db[key]
            return None
        return value


class SetCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = {"key", "value"}
    POSSIBLE_OPTIONS = {"EX", "PX", "EXAT", "PXAT"}

    def _calculate_expire(ex: int | None = None, px: int | None = None, exat: int | None = None, pxat: int | None = None) -> int:
        if ex is not None:
            return _get_current_time_in_ms() + int(ex) * 1000
        if px is not None:
            return _get_current_time_in_ms() + int(px)
        if exat is not None:
            return int(exat) * 1000
        if pxat is not None:
            return int(pxat)

    def execute(self) -> str:
        """SET key value [EX seconds] [PX milliseconds] [EXAT timestamp-seconds] [PXAT timestamp-ms] [NX|XX]"""
        self._parse_arguments()
        expire_attrs = {key.lower(): self.get(key) for key in self.POSSIBLE_OPTIONS}
        key, value = self.get("key"), self.get("value")
        expire = None
        if any(expire_attrs.values()):
            expire = self._calculate_expire(**expire_attrs)
        redis_db[key] = (str(value), expire)
        return "OK"
    

def get_command_handler(command: str) -> RedisCommand:
    command_map = {
        "PING": PingCommand,
        "ECHO": EchoCommand,
        "GET": GetCommand,
        "SET": SetCommand,
        "CLIENT": ClientCommand,
        "COMMAND": CommandCommand,
    }
    command_cls = command_map.get(command.upper())
    if not command_cls:
        raise UnknownCommandException(f"ERR Unsopported command `{command}`")
    return command_cls
