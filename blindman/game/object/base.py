
import numpy as np

from abc import ABC, abstractmethod


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
