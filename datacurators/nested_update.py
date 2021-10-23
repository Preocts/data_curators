from typing import Any
from typing import Mapping

__all__ = ["nested_update"]


def nested_update(
    map1: Mapping[Any, Any],
    map2: Mapping[Any, Any],
) -> Mapping[Any, Any]:
    """
    Merge two mappings, inluding nested mappings, returning a new result.

    This is done by starting with map1. Key/values that are unique
    to map2 are added. Key/values that exist in both are updated
    with map1[key] = map2[key]. Nested mapping structures have the
    same logic applied, recursively.
    """
    if not isinstance(map1, Mapping) or not isinstance(map2, Mapping):
        raise TypeError("Expected Mappings, got: %s, %s", type(map1), type(map2))

    result = {key: value for key, value in map1.items()}

    for key, value in map2.items():
        if key not in result:
            result[key] = value
        elif not isinstance(value, Mapping):
            result[key] = value
        else:
            result[key] = nested_update(result[key], value)

    return result
