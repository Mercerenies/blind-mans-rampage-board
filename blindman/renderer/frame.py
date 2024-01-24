
import numpy as np

from abc import ABC, abstractmethod


class FrameRenderer(ABC):

    @abstractmethod
    def total_frames(self) -> int:
        ...

    @abstractmethod
    def fps(self) -> int:
        ...

    @abstractmethod
    def frame_size(self) -> tuple[int, int]:
        """Returns (width, height) of the desired canvas."""
        ...

    @abstractmethod
    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        """Render to the canvas which contains the previous frame. The
        current contents of the canvas are unspecified if this is the
        first frame.

        """
        ...
