
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer, InputFile, Board, Timeline, GameEngine
from blindman.game.object import EventManager

if __name__ == "__main__":
    input_file = InputFile.read_file("example.lisp")

    # Set up the renderer and control objects.
    game_engine = GameEngine()
    event_manager = EventManager(game_engine)
    game_engine.add_object(event_manager)

    # Set up the timeline and board manager.
    timeline = Timeline(manager=event_manager)
    board = Board(
        spaces_map=input_file.spaces_map,
    )

    # Add initial objects to the game board.
    all_game_objects = []
    for obj in input_file.objects:
        game_obj = obj.to_game_object(input_file.spaces_map)
        all_game_objects.append(game_obj)
        board.add_player(
            player=game_obj,
            starting_space=obj.space_name,
        )

    # Position the players in the initial frame.
    for game_obj in all_game_objects:
        game_obj.position = board.get_position(game_obj.name)
        game_engine.add_object(game_obj)

    # Play out the commands in order.
    for command in input_file.commands:
        command.execute(board, timeline)

    game_renderer = GameRenderer(
        config=input_file.config,
        engine=game_engine,
        total_frames=timeline.moment,
    )
    video_renderer = VideoRenderer(frame_renderer=game_renderer)
    video_renderer.render('tmp.mp4')
    print("Done.")
