from resp.types import get_serializer_type
from typing import Any


def serialize(resp_obj: Any, use_bulk: bool = True, is_error: bool = False) -> str:
    resp_type = get_serializer_type(resp_obj, use_bulk, is_error)
    return resp_type.serialize(resp_obj)


