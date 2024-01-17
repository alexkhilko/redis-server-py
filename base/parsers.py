from typing import Any
import io


CRLF = b"\r\n"


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
            length = int(self._readline().decode("utf-8").rstrip('\r\n'))
            if length == -1:
                return None
            return [self.parse() for _ in range(length)]

        resp_type = self._buffer.read(1)

        if resp_type == b'+':
            return parse_simple_string()
        elif resp_type == b'-':
            return parse_error()
        elif resp_type == b':':
            return parse_integer()
        elif resp_type == b'$':
            return parse_bulk_string()
        elif resp_type == b'*':
            return parse_array()
        else:
            raise ValueError(f"Invalid RESP type: {resp_type}")
