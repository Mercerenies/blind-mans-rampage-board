
from blindman.renderer import VideoRenderer
from blindman.game import GameRenderer, InputFile, Board, Timeline, GameEngine
from blindman.game.object import EventManager

import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The input .lisp file to read')
    parser.add_argument('-o', '--output-filename', required=True, type=str, help='The output path to write to')
    return parser.parse_args()


def compile(input_file: InputFile, output_filename: str) -> None:

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
        board[game_obj.name] = obj.space_name

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
    video_renderer.render(output_filename)


if __name__ == "__main__":
    args = parse_args()
    input_file = InputFile.read_file(args.input_file)

    # Interpret relative paths in the .lisp file relative to its directory
    cwd = os.path.dirname(os.path.abspath(args.input_file))
    os.chdir(cwd)

    compile(input_file, args.output_filename)
    print("Done.")
