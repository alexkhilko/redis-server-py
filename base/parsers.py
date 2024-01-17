from typing import Any
import io
from base.exceptions import RespProtocolError, RespParsingError


CRLF = b"\r\n"
CRLF_STR = "\r\n"


class RespParser:
    def __init__(self, data: bytes, encoding: str = "utf-8"):
        self._buffer = io.BytesIO(data)
        self._encoding = encoding

    def _readline(self) -> bytes:
        data = self._buffer.readline()
        while not data.endswith(CRLF):
            data += self._readline()
        return data
    
    def _decode(self, data: bytes) -> str:
        return data.rstrip(CRLF).decode(self._encoding)

    def parse(self) -> Any:
        """Parse RESP data into Python object"""
        def parse_simple_string() -> str:
            return self._decode(self._readline())

        def parse_error() -> str:
            return self._decode(self._readline())

        def parse_integer() -> int:
            return int(self._decode(self._readline()))

        def parse_bulk_string() -> str:
            length = int(self._decode(self._readline()))
            if length == -1:
                return None
            # make sure to read CRLF 2 bytes
            return self._decode(self._buffer.read(length + 2))

        def parse_array() -> list[Any]:
            length = int(self._decode(self._readline()))
            if length == -1:
                return None
            return [self.parse() for _ in range(length)]

        resp_type = self._buffer.read(1)
        try:
            if resp_type == b'+':
                return parse_simple_string()
            if resp_type == b'-':
                return parse_error()
            if resp_type == b':':
                return parse_integer()
            if resp_type == b'$':
                return parse_bulk_string()
            if resp_type == b'*':
                return parse_array()
        except Exception as e:
            raise RespParsingError(f"Failed to parse resp data: {resp_type}") from e
        raise RespProtocolError(f"Unsopported RESP type: {resp_type}")


class RespSerializer:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def serialize(self, data, use_bulk=True, is_error=False) -> bytes:
        value = self._serialize(
            data=data, use_bulk=use_bulk, is_error=is_error
        )
        return value.encode(self.encoding)
    
    def _serialize(self, data, use_bulk=True, is_error=False) -> bytes:
        if is_error:
            return f"-{data}{CRLF_STR}"
        if data is None:
            return f"$-1{CRLF_STR}"
        if isinstance(data, str):
            return f"${len(data)}{CRLF_STR}{data}{CRLF_STR}" if use_bulk else f"+{data}{CRLF_STR}"
        if isinstance(data, int):
            return f":{data}{CRLF_STR}"
        if isinstance(data, (list, tuple)):
            result = [f"*{len(data)}{CRLF_STR}"]
            for item in data:
                result.append(self._serialize(data=item, use_bulk=use_bulk, is_error=False))
            return "".join(result)
        raise RespProtocolError(f"Unsupported RESP type: {type(data)}, {data}")
