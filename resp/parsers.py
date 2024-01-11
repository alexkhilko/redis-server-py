from resp.types import get_resp_type
from typing import Any


def deserialize(resp_str: str) -> Any:
    resp_type = get_resp_type(resp_str)
    return resp_type.deserialize(resp_str)[0]
