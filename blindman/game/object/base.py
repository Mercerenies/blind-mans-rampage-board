
import numpy as np

from abc import ABC, abstractmethod


class GameObject(ABC):

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
