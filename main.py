
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer, InputFile
from blindman.game.object import EventManager

input_file = InputFile.read_file("example.lisp")

game_renderer = GameRenderer(config=input_file.config)
video_renderer = VideoRenderer(frame_renderer=game_renderer)
for obj in input_file.objects:
    game_renderer.engine.add_object(obj.to_game_object())

event_manager = EventManager(game_renderer.engine)
game_renderer.engine.add_object(event_manager)
#event_manager.append_event(0, MoveObjectEvent.factory("star", (256, 256), 60))

video_renderer.render('tmp.mp4')
print("Done.")
