class RedisServerException(Exception):
    pass


class UnknownCommandException(RedisServerException):
    pass


class InvalidCommandSyntaxError(RedisServerException):
    pass


class RespProtocolError(RedisServerException):
    pass


class RespParsingError(RedisServerException):
    pass


class CommandProcessingException(RedisServerException):
    pass
