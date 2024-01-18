from abc import ABC, abstractmethod
from base.exceptions import InvalidCommandSyntaxError
from typing import Any


class RedisCommand(ABC):
    """
    Base class for all Redis commands.
    It provides basic functionality for parsing arguments and options.
    """
    #TODO: Add support for checking type of arguments
    REQUIRED_ATTRIBUTES: tuple
    POSSIBLE_OPTIONS: tuple

    def __init__(self, arguments):
        self._arguments = arguments
        self._attributes: dict = {}
    
    def _parse_arguments(self) -> None:
        arguments = self._arguments
        if len(arguments) < len(self.REQUIRED_ATTRIBUTES):
            raise InvalidCommandSyntaxError("ERR wrong number of arguments for command")
        idx = 0
        for key in self.REQUIRED_ATTRIBUTES:
            self._attributes[key] = arguments[idx]
            idx += 1

        if (len(arguments) - idx) % 2 != 0:
            raise InvalidCommandSyntaxError("ERR syntax error")

        for i in range(idx, len(arguments), 2):
            if arguments[i] not in self.POSSIBLE_OPTIONS:
                raise InvalidCommandSyntaxError(f"ERR invalid option: {arguments[i]}")
            self._attributes[arguments[i]] = arguments[i + 1]
        
    def get(self, key: str) -> Any:
        return self._attributes.get(key)

    @abstractmethod
    def execute(self) -> str:
        pass