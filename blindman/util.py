
import attrs

from typing import Iterable
from typing import TypeVar


_K = TypeVar("_K")
_V = TypeVar("_V")


def attrs_field_names(cls: type) -> list[str]:
    return [f.name for f in attrs.fields(cls)]


def pluck(dictionary: dict[_K, _V], keys: Iterable[_K]) -> dict[_K, _V]:
    return {k: dictionary[k] for k in keys if k in dictionary}
