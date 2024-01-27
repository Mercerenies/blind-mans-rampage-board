
from __future__ import annotations

from .text import draw_text, draw_text_multiline, TextAlign

import attrs
import numpy as np

from contextlib import contextmanager
import itertools
import os
from typing import Iterable, Iterator, TypeVar, Literal, overload, Generator

__all__ = (
    'MAX_BYTE', 'ALPHA_CHANNEL',
    'attrs_field_names', 'pluck', 'draw', 'lerp', 'batched', 'pairs',
    'draw_text', 'draw_text_multiline', 'TextAlign',
    'cwd',
)

MAX_BYTE = 255
ALPHA_CHANNEL = 3


_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

_T_number = TypeVar("_T_number", int, float)


def attrs_field_names(cls: type) -> list[str]:
    return [f.name for f in attrs.fields(cls)]


def pluck(dictionary: dict[_K, _V], keys: Iterable[_K]) -> dict[_K, _V]:
    return {k: dictionary[k] for k in keys if k in dictionary}


def draw(
        destination: np.ndarray,
        source: np.ndarray,
        center: tuple[int, int],
        *,
        alpha: float = 1.0,
) -> None:
    upperleft_y, upperleft_x = center[0] - source.shape[0] // 2, center[1] - source.shape[1] // 2
    lowerright_y, lowerright_x = upperleft_y + source.shape[0], upperleft_x + source.shape[1]
    destination_patch = destination[upperleft_y:lowerright_y, upperleft_x:lowerright_x, :]
    source_alpha = (source[:, :, (ALPHA_CHANNEL,)] / MAX_BYTE) * alpha
    destination_patch = destination_patch * (1 - source_alpha) + source * source_alpha
    destination[upperleft_y:lowerright_y, upperleft_x:lowerright_x, :] = destination_patch.astype(np.uint8)


def lerp(a: _T_number, b: _T_number, x: _T_number) -> _T_number:
    return (1 - x) * a + x * b


@overload
def batched(iterable: Iterable[_T], n: Literal[1]) -> Iterator[tuple[_T]]: ...
@overload
def batched(iterable: Iterable[_T], n: Literal[2]) -> Iterator[tuple[_T, _T]]: ...
@overload
def batched(iterable: Iterable[_T], n: Literal[3]) -> Iterator[tuple[_T, _T, _T]]: ...


def batched(iterable: Iterable[_T], n: int) -> Iterator[tuple[_T, ...]]:
    """Backport of itertools.batched from Python 3.12+"""
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def pairs(iterable: Iterable[_T]) -> Iterator[tuple[_T, _T]]:
    return batched(iterable, 2)


@contextmanager
def cwd(new_cwd: str) -> Generator[None, None, None]:
    old_cwd = os.getcwd()
    os.chdir(new_cwd)
    yield
    os.chdir(old_cwd)
