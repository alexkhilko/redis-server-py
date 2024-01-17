from base.exceptions import UnknownCommandException, RedisServerException
import logging
from base.parsers import RespParser, RespSerializer
import time

logger = logging.getLogger(__name__)


def _handle_request(data: bytes) -> list:
    command, *arguments = RespParser(data=data).parse()
    # logger.info("Received command %s, arguments %s", command, arguments)
    if command == "PING":
        return ["PONG"]
    if command == "ECHO":
        return arguments
    if command.upper() == "GET":
        return handle_get(arguments[0])
    if command.upper() == "SET":
        expire_attrs = {arguments[2].lower(): arguments[3]} if len(arguments) > 2 else {}
        return handle_set(key=arguments[0], value=arguments[1], **expire_attrs)
    if command.upper() in ["CLIENT", "COMMAND"]:
        # mock response, do not implement
        return ["OK"]
    raise UnknownCommandException(
        f"Unknown command `{command}`, arguments `{arguments}`"
    )


def process_request(request: bytes) -> bytes:
    try:
        response = _handle_request(request)
    except RedisServerException as exc:
        logger.exception("Redis exception - %s", exc)
        return RespSerializer().serialize([exc], is_error=True)
    return RespSerializer().serialize(response)


redis_db = {}


def _get_current_time_in_ms() -> int:
    return int(time.time()) * 1000


def handle_get(key: str) -> str | None:
    value, expires = redis_db.get(key, [None, None])
    if expires is not None and expires < _get_current_time_in_ms():
        del redis_db[key]
        return None
    return value


def _calculate_expire(ex: int | None = None, px: int | None = None, exat: int | None = None, pxat: int | None = None) -> int:
    if ex is not None:
        return _get_current_time_in_ms() + int(ex) * 1000
    if px is not None:
        return _get_current_time_in_ms() + int(px)
    if exat is not None:
        return int(exat) * 1000
    if pxat is not None:
        return int(pxat)


def handle_set(
        key,
        value,
        ex: int | None = None,
        px: int | None = None,
        exat: int | None = None,
        pxat: int | None = None,
    ) -> str:
    """SET key value [EX seconds] [PX milliseconds] [EXAT timestamp-seconds] [PXAT timestamp-ms] [NX|XX]"""
    expire = None
    if any([ex, px, exat, pxat]):
        expire = _calculate_expire(ex=ex, px=px, exat=exat, pxat=pxat)
    redis_db[key] = (str(value), expire)
    return "OK"
