from resp.parsers import deserialize
from exceptions import UnknownCommandException
import logging

logger = logging.getLogger(__name__)


def parse_request(request: bytes) -> str:
    return deserialize(request.decode("utf-8"))


def handle_request(data: bytes) -> list:
    command, *arguments = parse_request(request=data)
    logger.info("Received command %s, arguments %s", command, arguments)
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
    raise UnknownCommandException(f"Unknown command `{command}`, arguments `{arguments}`")


store = {}


def handle_get(key: str) -> str | None:
    return store.get(key)


def handle_set(key: str, value: str) -> str:
    "Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type."
    store[key] = str(value)
    return "OK"
