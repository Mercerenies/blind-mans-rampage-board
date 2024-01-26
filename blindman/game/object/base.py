
import numpy as np

from abc import ABC, abstractmethod


class GameObject(ABC):
    position: tuple[int, int]

    def __init__(self) -> None:
        self.position = (0, 0)

    @property
    @abstractmethod
    def name(self) -> str | None:
        ...

    @abstractmethod
    def step(self, frame_number: int) -> None:
        ...

    @abstractmethod
    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        ...
