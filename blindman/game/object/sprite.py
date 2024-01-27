
from .base import GameObject
from blindman.util import draw

from attrs import define
import numpy as np


@define(eq=False)
class Sprite(GameObject):
    position: tuple[int, int]
    image: np.ndarray
    _name: str

    def __attrs_pre_init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    def step(self, frame_number: int) -> None:
        pass  # Sprites are static objects; they do not move on their own

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        draw(canvas, self.image, self.position)
