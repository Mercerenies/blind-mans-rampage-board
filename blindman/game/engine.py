
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .object import GameObject

import numpy as np

from copy import copy


class GameEngine:
    """Game engine, which maintains a collection of objects and
    invokes their callbacks when appropriate."""

    _objects: list[GameObject]

    def __init__(self) -> None:
        self._objects = []

    def perform_step(self, frame_number: int) -> None:
        for obj in copy(self._objects):  # copy: Do not reflect changes to the list during iteration.
            obj.step(frame_number)

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        for obj in copy(self._objects):  # copy: Do not reflect changes to the list during iteration.
            obj.draw(frame_number, canvas)

    def add_object(self, obj: GameObject) -> None:
        self._objects.append(obj)

    def remove_object(self, obj: GameObject | str) -> None:
        if isinstance(obj, str):
            obj = self.find_object(obj)
        self._objects.remove(obj)

    def has_object(self, name: str) -> bool:
        return any(obj.name == name for obj in self._objects)

    def find_object(self, name: str) -> GameObject:
        for obj in self._objects:
            if obj.name == name:
                return obj
        raise ValueError(f"Object with name '{name}' not found")
