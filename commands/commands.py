import time
from commands.base import RedisCommand
from base.exceptions import CommandProcessingException
from collections import deque


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


def check_expires(expires: int | None) -> bool:
    return expires is not None and expires < _get_current_time_in_ms()


class GetCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ["key"]

    def execute(self) -> str:
        self._parse_arguments()
        key = self.get("key")
        value, expires = redis_db.get(key, [None, None])
        if expires is not None and expires < _get_current_time_in_ms():
            del redis_db[key]
            return None
        return value


class SetCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ["key", "value"]
    POSSIBLE_OPTIONS = ["EX", "PX", "EXAT", "PXAT"]

    def _calculate_expire(self, ex: int | None = None, px: int | None = None, exat: int | None = None, pxat: int | None = None) -> int:
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
        print(f"setting {key} to {value} with expire {expire}")
        return "OK"
    
    
class ExistsCommand(RedisCommand):
    def execute(self):
        number = 0
        for key in self._arguments:
            if key not in redis_db:
                continue
            _, expires = redis_db[key]
            if check_expires(expires):
                del redis_db[key]
                continue
            number += 1
        return number


class DeleteCommand(RedisCommand):
    def execute(self) -> str:
        number = 0
        for key in self._arguments:
            if key not in redis_db:
                continue
            del redis_db[key]
            number += 1
        return number
    

def _increment(key: str, increment: int) -> int:
    value, expires = redis_db.get(key, [None, None])
    if value is None or check_expires(expires):
        redis_db[key] = (1, None)
        return increment
    try:
        value = int(value)
    except ValueError as e:
        raise CommandProcessingException("ERR value is not an integer or out of range") from e
    redis_db[key] = value + increment, expires
    return value + increment


class IncrCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ["key"]

    def execute(self) -> str:
        self._parse_arguments()
        key = self.get("key")
        return _increment(key, increment=1)


class IncrByCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ["key", "increment"]

    def execute(self) -> str:
        self._parse_arguments()
        key, increment = self.get("key"), self.get("increment")
        return _increment(key, increment=int(increment))


class DecrCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ["key"]

    def execute(self) -> str:
        self._parse_arguments()
        key = self.get("key")
        return _increment(key, increment=-1)


class DecrByCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ["key", "decrement"]

    def execute(self) -> str:
        self._parse_arguments()
        key, decrement = self.get("key"), self.get("decrement")
        print(decrement)
        return _increment(key, increment=-int(decrement))


class LPushCommand(RedisCommand):
    def execute(self) -> str:
        key, *values = self._arguments
        value, expires = redis_db.get(key, [None, None])
        if value is None or check_expires(expires):
            value = deque(values)
        else:
            if not isinstance(value, deque):
                raise CommandProcessingException("WRONGTYPE Operation against a key holding the wrong kind of value")
            for val in values:
                value.appendleft(val)
        redis_db[key] = (value, None)
        return len(value)
