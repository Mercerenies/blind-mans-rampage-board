
from blindman.discord import get_avatar
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer

renderer = VideoRenderer(
    frame_renderer=GameRenderer(),
)

renderer.render('tmp.mp4')
print("Done.")
