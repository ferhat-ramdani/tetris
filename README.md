# Tetris Game

## How to play ?

- Use `⬅️` and `➡️` keys to move the pieces left and right.
- Use the `space` key to rotate the pieces.
- Use the `⬇️` key to accelerate the fall of the pieces.

## Try it !

you can try it here (only works on laptop) : https://tetris-s5wj.onrender.com

## Options

- Use `--log <file>` to specify a file where logs will be written. Logs are stored inside the folder `log`. When the user does not specify the log file, a default log file with the name `game.log` will be created and used.
- Use `--seed <seed>`to specify a seed for the random number generator.
- Use `--piece <pieces_folder>` or `-p <pieces_folder>` to specify a folder containing the pieces of the game.
- Use `--speed <speed>` or `-s <speed>` to specify the speed of the game at the start. Allowed values are `slow`, `medium` and `fast`.
- Use `--width <width>` or `-w <width>` to specify the width of the game.
- Use `--height <height>` or `-h <height>` to specify the height of the game.
- Use `--no-color` to disable colored pieces. By default, the pieces are colored.

## Launch the game

### On Windows
Simply double-click the `launch.bat` file in the project folder. This will automatically handle setting up the virtual environment, installing dependencies, and launching the game.

### On Linux/Mac
1. Make the script executable (only needed once): `chmod +x launch.sh`
2. Run the script: `./launch.sh`

This script will automatically handle setting up the virtual environment, installing dependencies, and launching the game.
