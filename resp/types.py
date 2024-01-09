from abc import abstractmethod
from typing import Any


CRLF = "\r\n"


class RespType:
    @staticmethod
    def _get_clean_value(value: str) -> str:
        return value.removesuffix(CRLF)

    @staticmethod
    @abstractmethod
    def serialize(value: Any) -> str:
        """convert object to RESP string"""
    
    @staticmethod
    @abstractmethod
    def deserialize(value: str) -> Any:
        """convert RESP string to object"""


class SimpleString(RespType):
    @staticmethod
    def serialize(value: str) -> str:
        return f"+{value}{CRLF}"
    
    @staticmethod
    def deserialize(value: str) -> str:
        return str(value.removeprefix("+"))


class SimpleError(RespType):
    @staticmethod
    def serialize(value: str) -> str:
        return f"-{value}{CRLF}"
    
    @staticmethod
    def deserialize(value: str) -> str:
        return str(value.removeprefix("-"))


class Integer(RespType):
    @staticmethod
    def serialize(value: int) -> str:
        return f":{value}{CRLF}"
    
    @staticmethod
    def deserialize(value: str) -> int:
        return int(value)


class BulkString(RespType):
    @staticmethod
    def serialize(value: str) -> str:
        return f"${len(value)}{CRLF}{value}{CRLF}"
    
    @staticmethod
    def deserialize(value: str) -> str:
        data = value.split(CRLF, 1)[1]
        return str(data)
    

class Array(RespType):
    @staticmethod
    def serialize(value: list) -> str:
        data = []
        for element in value:
            resp_type = get_resp_type(element)
            data.append(resp_type.serialize(element))
        return f"*{''.join(data)}{CRLF}"
    
    @staticmethod
    def deserialize(value: str) -> list:
        """*<number-of-elements>\r\n<element-1>...<element-n>"""
        elements = value.split(CRLF)
        data_elements = elements[1:]
        data = []
        for element in data_elements:
            resp_type = get_resp_type(element)
            data.append(resp_type.deserialize(element))
        return data


def get_resp_type(resp_string: str) -> RespType:
    start_byte = resp_string[0]
    if start_byte == "+":
        return "string"
    if start_byte == "-":
        return "simple error"
    if start_byte == ":":
        return "integer"
    if start_byte == "$":
        return "bulk string"
    if start_byte == "*":
        return "array"
    raise ValueError(f"Unknown type for {resp_string}")
