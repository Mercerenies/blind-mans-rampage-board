
from blindman.discord import get_avatar
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer, Configuration
from blindman.lisp import parse_many

test_str = """
(configuration
  :background-image "/home/silvio/Pictures/BlindMansRampage/Game1/Floor1/BlindManFloor1_DEBUG.png")
"""

parsed_file = parse_many(test_str)

renderer = VideoRenderer(
    frame_renderer=GameRenderer(config=Configuration.from_sexpr(parsed_file[0])),
)

renderer.render('tmp.mp4')
print("Done.")
