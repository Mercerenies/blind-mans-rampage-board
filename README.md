# Blind Man's Rampage Video Generator

This library produces video files replaying a game of Blind Man's
Rampage.

## Usage

    python3 main.py <input_filename> -o <output_filename>

`input_filename` should be the name of a `.lisp` file, and
`output_filename` should be the name of the desired result video file.
All output file formats supported by the `imageio` Python library are
supported, though this software has been mostly tested with `.mp4`
files.

If you wish to reference Discord avatars in the input file, you will
need to register a Discord bot application and set the
`DISCORD_BOT_TOKEN` environment variable to the application's bot
token. In that case, it is also recommended (but not required) that
you have a local Redis server running on `localhost:6379`. If present,
Redis will be used to cache Discord avatars and avoid unnecessarily
hitting the Discord servers.

See `example.lisp` for an annotated example input file.
