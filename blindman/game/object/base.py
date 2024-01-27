
import numpy as np

from abc import ABC, abstractmethod


class GameObject(ABC):
    """An object in the game room."""

    @property
    @abstractmethod
    def name(self) -> str | None:
        """Game objects can optionally have a name, to make it easier
        to identify. If a game object has a name, it must be
        globally unique among the objects in the room.

        """
        ...

    @abstractmethod
    def step(self, frame_number: int) -> None:
        """Performs the object's step event for the given frame
        number."""
        ...

    @abstractmethod
    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        """Draws the object to the canvas."""
        ...
