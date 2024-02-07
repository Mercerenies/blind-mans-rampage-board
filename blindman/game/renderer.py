
from .input import Configuration
from .engine import GameEngine
from blindman.renderer import FrameRenderer

import numpy as np
from attrs import define, field


@define(eq=False)
class GameRenderer(FrameRenderer):
    """A FrameRenderer for rendering the game room based on a
    GameEngine.

    """

    config: Configuration = field()
    engine: GameEngine = field()
    width: int
    height: int
    _total_frames: int = field()

    def total_frames(self) -> int:
        return self._total_frames

    def fps(self) -> int:
        return self.config.fps

    def frame_size(self) -> tuple[int, int]:
        return self.width, self.height

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        # Run one step of the game engine
        self.engine.perform_step(frame_number)

        # Now draw everything
        self.engine.render_frame(frame_number, canvas)
