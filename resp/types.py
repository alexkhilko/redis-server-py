from typing import Any


CRLF = "\r\n"

RETURN_TYPE = tuple[Any, str]


class RespType:
    START_BYTE = None

    @classmethod
    def serialize(cls, value: Any) -> str:
        """convert object to RESP string"""
        return f"{cls.START_BYTE}{cls._serialize(value)}{CRLF}"

    @classmethod
    def _serialize(cls, value: str) -> str:
        return value

    @classmethod
    def deserialize(cls, value: str) -> RETURN_TYPE:
        """convert RESP string to object"""
        value = value.removeprefix(cls.START_BYTE)
        return cls._deserialize(value)

    @classmethod
    def _deserialize(cls, value: str) -> RETURN_TYPE:
        return value.split(CRLF, 1)


class SimpleString(RespType):
    START_BYTE = "+"


class SimpleError(RespType):
    START_BYTE = "-"


class Integer(RespType):
    START_BYTE = ":"

    @classmethod
    def _deserialize(cls, value: str) -> RETURN_TYPE:
        value, remaining = super()._deserialize(value)
        return int(value), remaining


class BulkString(RespType):
    START_BYTE = "$"

    @classmethod
    def _serialize(cls, value: str) -> str:
        if value is None:
            return "-1"
        return f"{len(value)}{CRLF}{value}"

    @classmethod
    def _deserialize(cls, value: str) -> RETURN_TYPE:
        length, data = value.split(CRLF, 1)
        length = int(length)
        if length == -1:
            return None, data.removeprefix(CRLF)
        return data[:length], data[length:].removeprefix(CRLF)


class Array(RespType):
    START_BYTE = "*"

    @classmethod
    def serialize(cls, value: list) -> str:
        data = []
        for element in value:
            resp_type = get_serializer_type(element, use_bulk=True)
            data.append(resp_type.serialize(element))
        return f"{cls.START_BYTE}{len(data)}{CRLF}{''.join(data)}"

    @classmethod
    def _deserialize(cls, value: str) -> RETURN_TYPE:
        number_of_elements, elements_str = value.split(CRLF, 1)
        number_of_elements = int(number_of_elements)
        if number_of_elements == -1:
            return None, elements_str.removeprefix(CRLF)
        data = []
        while number_of_elements:
            resp_type = get_deserializer_type(elements_str)
            element, elements_str = resp_type.deserialize(elements_str)
            data.append(element)
            number_of_elements -= 1
        return data, elements_str


def get_deserializer_type(resp_string: str) -> RespType:
    start_byte = resp_string[0]
    if start_byte == "+":
        return SimpleString()
    if start_byte == "-":
        return SimpleError()
    if start_byte == ":":
        return Integer()
    if start_byte == "$":
        return BulkString()
    if start_byte == "*":
        return Array()
    raise ValueError(f"Unknown RESP type: {start_byte}")


def get_serializer_type(
    obj: Any, use_bulk: bool = False, is_error: bool = False
) -> RespType:
    if obj is None:
        return BulkString()
    if isinstance(obj, str):
        if is_error:
            return SimpleError()
        # TODO: Think about a better way to define what type to use for strings.
        return SimpleString() if not use_bulk else BulkString()
    if isinstance(obj, int):
        return Integer()
    if isinstance(obj, list):
        return Array()
    raise ValueError(f"Unknown RESP type: {type(obj)}")
