
from .base import GameObject
from blindman.util import draw_text_multiline, TextAlign

import numpy as np
import cv2
from attrs import define, field

BOTTOM_TEXT_OBJECT_NAME = "__bottomtext"
TEXT_Z_INDEX = 10
SOLID_BLACK = (0, 0, 0, 255)

Color = tuple[int, int, int, int]


@define(eq=False)
class BottomText(GameObject):
    """Singleton object which draws text at the lower-center of the
    grid. Only one can exist per GameEngine at a time."""
    text: str = field()
    font: int = field(kw_only=True, default=cv2.FONT_HERSHEY_SIMPLEX)
    font_scale: float = field(kw_only=True, converter=float, default=0.75)
    thickness: int = field(kw_only=True, default=2)
    color: Color = field(kw_only=True, default=SOLID_BLACK)
    offset_from_bottom: int = field(kw_only=True, default=32)

    def __attrs_pre_init__(self) -> None:
        super().__init__()

    @property
    def z_index(self) -> int:
        return TEXT_Z_INDEX

    @property
    def name(self) -> str:
        return BOTTOM_TEXT_OBJECT_NAME

    def step(self, frame_number: int) -> None:
        pass  # Status text is a static object; it does not move on its own

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        display_height, display_width, _ = canvas.shape
        draw_text_multiline(
            image=canvas,
            text=self.text,
            origin=(display_height - self.offset_from_bottom, display_width // 2),
            align=TextAlign.BOTTOM_CENTER,
            font=self.font,
            color=self.color,
            font_scale=self.font_scale,
            thickness=self.thickness,
        )
