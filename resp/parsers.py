from resp.types import get_deserializer_type, get_serializer_type
from typing import Any


def deserialize(resp_str: str) -> Any:
    resp_type = get_deserializer_type(resp_str)
    return resp_type.deserialize(resp_str)[0]


def serialize(resp_obj: Any, use_bulk: bool = True, is_error: bool = False) -> str:
    resp_type = get_serializer_type(resp_obj, use_bulk, is_error)
    return resp_type.serialize(resp_obj)


