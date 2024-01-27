
import numpy as np

from abc import ABC, abstractmethod


class FrameRenderer(ABC):
    """The backend for a VideoRenderer. A FrameRenderer determines
    certain configuration parameters about the resulting video and
    defines how to render each individual frame to the video.

    """

    @abstractmethod
    def total_frames(self) -> int:
        """The total number of frames desired in the resulting video."""
        ...

    @abstractmethod
    def fps(self) -> int:
        """Frames per second of the resulting video."""
        ...

    @abstractmethod
    def frame_size(self) -> tuple[int, int]:
        """Returns (height, width) of the desired canvas."""
        ...

    @abstractmethod
    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        """Render to the canvas which contains the previous frame. The
        current contents of the canvas are unspecified if this is the
        first frame.

        Implementors are guaranteed that this method will be called in
        order from frame zero up to, and excluding,
        self.total_frames().

        """
        ...
