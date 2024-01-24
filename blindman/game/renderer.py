
from blindman.renderer import FrameRenderer

import numpy as np


class GameRenderer(FrameRenderer):

    def total_frames(self) -> int:
        return 30

    def fps(self) -> int:
        return 30

    def frame_size(self) -> tuple[int, int]:
        return (512, 512)

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        canvas[:] = 255
