
from __future__ import annotations

import numpy as np

from abc import ABC, abstractmethod


class GameEngine:
    _objects: list[GameObject]

    def __init__(self) -> None:
        self._objects = []

    def perform_step(self, frame_number: int) -> None:
        for obj in self._objects:
            obj.step(frame_number)

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        for obj in self._objects:
            obj.draw(frame_number, canvas)

    def add_object(self, obj: GameObject) -> None:
        self._objects.append(obj)

    def remove_object(self, obj: GameObject) -> None:
        self._objects.remove(obj)

    def find_object(self, name: str) -> GameObject:
        for obj in self._objects:
            if obj.name == name:
                return obj
        raise ValueError(f"Object with name '{name}' not found")


class GameObject(ABC):
    name: str | None

    def __init__(self, name: str | None = None) -> None:
        self.name = name

    @abstractmethod
    def step(self, frame_number: int) -> None:
        ...

    @abstractmethod
    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        ...
