
#from blindman.discord import get_avatar
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer, Configuration
from blindman.game.object import Sprite, EventManager, MoveObjectEvent
from blindman.lisp import parse_many

import cv2

test_str = """
(configuration
  :background-image "/home/silvio/Pictures/BlindMansRampage/Game1/Floor1/BlindManFloor1_DEBUG.png")
"""
star = cv2.imread("/home/silvio/Documents/star.png", cv2.IMREAD_UNCHANGED)
star = cv2.cvtColor(star, cv2.COLOR_BGRA2RGBA)

parsed_file = parse_many(test_str)

game_renderer = GameRenderer(config=Configuration.from_sexpr(parsed_file[0]))
video_renderer = VideoRenderer(frame_renderer=game_renderer)
game_renderer.engine.add_object(Sprite((96, 96), star, "star"))

event_manager = EventManager(game_renderer.engine)
game_renderer.engine.add_object(event_manager)
event_manager.append_event(0, MoveObjectEvent.factory("star", (256, 256), 60))

video_renderer.render('tmp.mp4')
print("Done.")
