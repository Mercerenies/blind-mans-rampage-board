
from .base import GameObject
from blindman.util import draw

import numpy as np


class Sprite(GameObject):
    _name: str
    image: np.ndarray

    def __init__(self, position: tuple[int, int], image: np.ndarray, name: str) -> None:
        super().__init__()
        self._name = name
        self.image = image
        self.position = position

    @property
    def name(self) -> str:
        return self._name

    def step(self, frame_number: int) -> None:
        pass  # Sprites are static objects; they do not move on their own

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        draw(canvas, self.image, self.position)
