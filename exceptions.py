class RedisServerException(Exception):
    pass


class UnknownCommandException(RedisServerException):
    pass
