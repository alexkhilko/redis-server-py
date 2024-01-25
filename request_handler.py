import logging

from base.exceptions import RedisServerException
from base.parsers import RespParser, RespSerializer
from commands import get_command_handler

logger = logging.getLogger(__name__)


def _handle_request(data: bytes) -> list:
    command, *arguments = RespParser(data=data).parse()
    command_handler = get_command_handler(command)
    return command_handler(arguments).execute()


def process_request(request: bytes) -> bytes:
    try:
        response = _handle_request(request)
    except RedisServerException as exc:
        logger.exception("Redis exception - %s", exc)
        return RespSerializer().serialize([exc], is_error=True)
    return RespSerializer().serialize(response)
