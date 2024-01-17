from abc import ABC, abstractmethod
from base.exceptions import InvalidCommandSyntaxError
from typing import Any


class RedisCommand(ABC):
    REQUIRED_ATTRIBUTES: set = set()
    POSSIBLE_OPTIONS: set = set()

    def __init__(self, *arguments):
        self._arguments = list(arguments)
        self._attributes: dict = {}
    
    def _parse_arguments(self):
        arguments = self._arguments[:]
        if len(arguments) < len(self.REQUIRED_ATTRIBUTES):
            raise InvalidCommandSyntaxError("ERR wrong number of arguments for command")
        for key in self.REQUIRED_ATTRIBUTES:
            self._attributes[key] = arguments.pop(0)
        if len(arguments) % 2 != 0:
            raise InvalidCommandSyntaxError("ERR syntax error")
        for i in range(0, len(arguments), 2):
            if arguments[i] in self.POSSIBLE_OPTIONS:
                self._attributes[arguments[i]] = arguments[i + 1]
            else:
                raise InvalidCommandSyntaxError(f"ERR invalid option {arguments[i]}")
        
    def get(self, key: str) -> Any:
        return self._attributes.get(key)

    @abstractmethod
    def execute(self) -> str:
        pass