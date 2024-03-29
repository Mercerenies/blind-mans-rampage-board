
from __future__ import annotations

from .frame import FrameRenderer

import imageio.v2 as iio
import numpy as np

from typing import Any, BinaryIO

COLOR_CHANNELS = 4  # RGBA


class VideoRenderer:
    """This class is responsible for actually producing the video,
    given a FrameRenderer capable of drawing the individual frames.

    """

    def __init__(self, frame_renderer: FrameRenderer) -> None:
        self._frame_renderer = frame_renderer

    def render(self, output_file: str | BinaryIO) -> None:
        """Renders the video to the given sink. If output_file is a
        string, it is treated as a filename. Otherwise, it is treated
        as a binary file-like output object.

        """
        height, width = self._frame_renderer.frame_size()
        canvas = np.zeros((height, width, COLOR_CHANNELS), dtype=np.uint8)
        writer: Any  # __enter__ type is wrong in imageio pyi
        with iio.get_writer(output_file, fps=self._frame_renderer.fps()) as writer:
            for i in range(self._frame_renderer.total_frames()):
                self._frame_renderer.render_frame(i, canvas)
                writer.append_data(canvas)
