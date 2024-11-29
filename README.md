# Python_2024_2025_Ramdani_Arbouche

# How to play ?

- Use `⬅️` and `➡️` keys to move the pieces left and right.
- Use the `space` key to rotate the pieces.
- Use the `⬇️` key to accelerate the fall of the pieces.

# Options

- Use `--log <file>` to specify a file where logs will be written. Logs are stored inside the folder `log`. When the user does not specify the log file, a default log file with the name `game.log` will be created and used.
- Use `--seed <seed>`to specify a seed for the random number generator.
- Use `--piece <pieces_folder>` or `-p <pieces_folder>` to specify a folder containing the pieces of the game.
- Use `--speed <speed>` or `-s <speed>` to specify the speed of the game at the start. Allowed values are `slow`, `medium` and `fast`.
- Use `--width <width>` or `-w <width>` to specify the width of the game.
- Use `--height <height>` or `-h <height>` to specify the height of the game.
- Use `--no-color` to disable colored pieces. By default, the pieces are colored.

# Launch the game

- Go to `src` folder
- Use `python3 tetris.py` to launch the game with default options.

> **Note:** This game is, for now, not supported in windows, since it uses the `curses` python library.
