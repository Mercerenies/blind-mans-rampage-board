
import attrs
import numpy as np
import cv2

from typing import Iterable
from typing import TypeVar


_K = TypeVar("_K")
_V = TypeVar("_V")


def attrs_field_names(cls: type) -> list[str]:
    return [f.name for f in attrs.fields(cls)]


def pluck(dictionary: dict[_K, _V], keys: Iterable[_K]) -> dict[_K, _V]:
    return {k: dictionary[k] for k in keys if k in dictionary}


def cv2_correct_rgb(arr: np.ndarray) -> None:
    arr[:] = arr[:, :, ::-1]


def imread_rgb(filename: str) -> np.ndarray:
    """As cv2.imread, but returns the numpy array in RGB order rather
    than BGR."""
    image_arr = cv2.imread(filename)
    cv2_correct_rgb(image_arr)
    return image_arr
