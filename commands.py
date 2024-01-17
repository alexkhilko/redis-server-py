from resp.parsers import serialize
from exceptions import UnknownCommandException
import logging
from exceptions import RedisServerException
from base.parsers import RespParser

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
        return handle_set(arguments[0], arguments[1])
    if command.upper() in ["CLIENT", "COMMAND"]:
        # mock response, do not implement
        return ["OK"]
    raise UnknownCommandException(
        f"Unknown command `{command}`, arguments `{arguments}`"
    )


def _encode_response(data: list) -> bytes:
    return serialize(data).encode("utf-8")


def _encode_error_response(error) -> bytes:
    return serialize([error], is_error=True).encode("utf-8")


def process_request(request: bytes) -> bytes:
    try:
        response = _handle_request(request)
    except RedisServerException as exc:
        logger.exception("Redis exception - %s", exc)
        response = _encode_error_response(str(exc))
    else:
        response = _encode_response(response)
    return response


store = {}


def handle_get(key: str) -> str | None:
    return store.get(key)


def handle_set(key: str, value: str) -> str:
    "Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type."
    store[key] = str(value)
    return "OK"
