
from __future__ import annotations

import attrs
import numpy as np

from typing import Iterable
from typing import TypeVar

MAX_BYTE = 255
ALPHA_CHANNEL = 3


_K = TypeVar("_K")
_V = TypeVar("_V")


def attrs_field_names(cls: type) -> list[str]:
    return [f.name for f in attrs.fields(cls)]


def pluck(dictionary: dict[_K, _V], keys: Iterable[_K]) -> dict[_K, _V]:
    return {k: dictionary[k] for k in keys if k in dictionary}


def draw(destination: np.ndarray, source: np.ndarray, center: tuple[int, int]) -> None:  # Takes (x, y)
    upperleft_y, upperleft_x = center[0] - source.shape[0] // 2, center[1] - source.shape[1] // 2
    lowerright_y, lowerright_x = upperleft_y + source.shape[0], upperleft_x + source.shape[1]
    destination_patch = destination[upperleft_y:lowerright_y, upperleft_x:lowerright_x, :]
    source_alpha = source[:, :, (ALPHA_CHANNEL,)] / MAX_BYTE
    destination_patch = destination_patch * (1 - source_alpha) + source * source_alpha
    destination[upperleft_y:lowerright_y, upperleft_x:lowerright_x, :] = destination_patch.astype(np.uint8)
