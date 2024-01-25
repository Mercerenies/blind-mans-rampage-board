
"""Helpers for deserializing Lisp-ish data into Python classes."""

from .symbol import Symbol
import blindman.util as util

from typing import Any, Callable


def basic_normalize_key(key: str) -> str:
    """Basic normalization, removes a leading colon if present and
    replaces dashes with underscores."""
    if key.startswith(':'):
        key = key[1:]
    return key.replace('-', '_')


def parse_key_value_list(
        sexpr: Any,
        *,
        header_key: str | None = "_type",
        require_symbol_keys: bool = True,
        normalize_key_function: Callable[[str], str] = basic_normalize_key,
) -> dict[str, Any]:
    """Accepts an S-expression of the form (header :key1 value1 :key2
    value2 ...) and returns a dictionary representing the same data.
    By default, the header is saved in a key called "_type", but that
    name can be changed, or the header can be omitted entirely.

    Parameters:

    * sexpr: The S-expression to be parsed.

    * header_key: If not None, then the header will be stored in this
      key. If None, no header will be parsed.

    * require_symbol_keys: If True (the default), throws an exception
      if a key is non-symbol.

    * key_normalize_function: Function to normalize key names before
      insertion into the dictionary.

    """
    if not isinstance(sexpr, list):
        raise DeserializeError(f"Expected list, got {sexpr}")

    result: dict[str, Any]
    result = {}

    # Parse header
    if header_key is not None:
        if len(sexpr) == 0:
            raise DeserializeError("Expected header, got empty list")
        if not isinstance(sexpr[0], Symbol):
            raise DeserializeError(f"Expected symbol for header, got {sexpr[0]}")
        result[header_key] = str(sexpr[0])
        sexpr = sexpr[1:]

    # Parse fields
    if len(sexpr) % 2 != 0:
        raise DeserializeError("Expected even number of key-values pairs in deserialize")
    for k, v in util.pairs(sexpr):
        if require_symbol_keys and not isinstance(k, Symbol):
            raise DeserializeError(f"Expected symbol for key, got {k}")
        k = normalize_key_function(str(k))
        if k in result:
            raise DeserializeError(f"Duplicate key {k} in deserialize")
        result[k] = v
    return result


class DeserializeError(Exception):
    pass
