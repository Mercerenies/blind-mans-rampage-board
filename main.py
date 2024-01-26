
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer, InputFile, Board, Timeline
from blindman.game.object import EventManager

if __name__ == "__main__":
    input_file = InputFile.read_file("example.lisp")

    # Set up the renderer and control objects.
    game_renderer = GameRenderer(config=input_file.config)
    event_manager = EventManager(game_renderer.engine)
    game_renderer.engine.add_object(event_manager)

    # Set up the timeline and board manager.
    timeline = Timeline(manager=event_manager)
    board = Board(
        delegate=timeline,
        spaces_map=input_file.spaces_map,
    )

    # Add initial objects to the game board.
    for obj in input_file.objects:
        game_obj = obj.to_game_object(input_file.spaces_map)
        game_renderer.engine.add_object(game_obj)
        board.add_player(game_obj, input_file.config.start_space, silently=True)

    print(board)

    video_renderer = VideoRenderer(frame_renderer=game_renderer)
    video_renderer.render('tmp.mp4')
    print("Done.")
