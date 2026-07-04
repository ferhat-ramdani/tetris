<p align="center">
  <a href="https://sonarcloud.io/summary/new_code?id=ferhat-ramdani_tetris">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=ferhat-ramdani_tetris&metric=alert_status" alt="Quality Gate Status" />
  </a>
</p>

# Tetris Game
<p align="center">
  <img width="406" height="400" alt="termtris" src="https://github.com/user-attachments/assets/57091f40-8500-41e9-a64e-280186282543" />
</p>

Welcome to **Termtris**! This is a modern take on the classic Tetris game, played right in your terminal, with several new features and quality-of-life improvements.

## Try it !

You can try it here (only works on laptop) : https://tetris-s5wj.onrender.com

## What's New (Features)
Unlike the classic Tetris game, this version comes packed with some exciting modern features:

* **AI Auto-Play**: Watch the computer play for you! An integrated AI solver can take control and calculate the best moves step-by-step.
* **Colors**: Pieces are beautifully colored by default for better visibility and a modern feel (can be disabled in options).
* **Shadow Preview**: A helpful shadow outline appears at the bottom of the grid, showing exactly where your current piece will land.
* **Ghost Pieces**: A special mode where you can instantly solidify ghost pieces in place. 

## How to Play (Controls)

The controls have been updated to support the new mechanics:

* `⬅️` / `➡️` : Move the piece left or right.
* `⬇️` : Soft Drop (accelerates the fall of the piece).
* `⬆️` : Hard Drop (instantly drops the piece to the shadow position). If Ghost Pieces are enabled, it instantly solidifies them in place!
* `SPACE` : Rotate the piece.
* `M` / `Q` / `ESC` : Return to the main menu.

## Options & Settings

When you launch the game, you'll be greeted with an interactive menu. You can customize:
- **Speed**: Choose between slow, medium, and fast.
- **Grid Size (Width & Height)**: Adjust the dimensions of your playing field.
- **Colors**: Toggle colored pieces on or off.
- **Play Mode**: Switch between manual Player mode and AI mode.
- **Shadow Preview**: Enable or disable the shadow piece indicator.
- **Ghost Pieces**: Enable or disable the ghost pieces feature.

*(Note: Command line arguments like `--log`, `--seed`, `--piece` are also supported for advanced configuration).*

## How the AI Works

The AI Auto-Play feature uses a powerful heuristic approach known as the **Pierre Dellacherie Algorithm**. Instead of looking many steps ahead, it evaluates the immediate best move for the current piece.

### Evaluation Process

For every new piece, the AI simulates dropping it in every possible rotation and across every column. It then scores the resulting board state based on six key metrics (where `+` is rewarded and `-` is penalized):

1. **Landing Height** (`-`) : Prefers keeping the stack as low as possible.
2. **Eroded Pieces** (`+`) : Rewards clearing lines, especially when the current piece contributes to it.
3. **Row Transitions** (`-`) : Penalizes jagged horizontal edges.
4. **Column Transitions** (`-`) : Penalizes jagged vertical edges.
5. **Holes** (`-`) : Heavily penalizes creating empty spaces trapped beneath blocks.
6. **Wells** (`-`) : Penalizes creating deep, narrow empty columns.

The AI simply picks the placement with the highest resulting score and executes the moves step-by-step.

## Launch the game

### On Windows
Simply double-click the `launch.bat` file in the project folder. This will automatically handle setting up the virtual environment, installing dependencies, and launching the game.

### On Linux/Mac
1. Make the script executable (only needed once): `chmod +x launch.sh`
2. Run the script: `./launch.sh`

This script will automatically handle setting up the virtual environment, installing dependencies, and launching the game.
