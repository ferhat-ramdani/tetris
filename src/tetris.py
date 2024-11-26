
"""The main module that runs the game."""

import curses
import random
import logging
import os

from argparser import Arguments
from pieces import read_pieces
from gui import GameWindow
from grid import Grid
from utils import generate_seed

logger = logging.getLogger(__name__)

# to manage screen display
COLS = 10
ROWS = 20
MARGIN = 20

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PIECES_FOLDER = os.path.join(CURRENT_PATH, '../pieces')
DEFAULT_LOG_DIR = os.path.join(CURRENT_PATH, '../log/')
DEFAULT_LOG_FIL = os.path.join(CURRENT_PATH, '../log/game.log')

def game_loop(pieces_folder: str,
              speed: str,
              width: int,
              height: int
              ):
    """The main game loop that runs until the game is over."""
    pieces = read_pieces(pieces_folder)
    grid = Grid(height, width)
    gui = GameWindow(window, MARGIN, speed)

    current_piece = random.choice(pieces)
    logger.info("Generated piece %s", current_piece)

    while True:
        position = list((0, width // 2 - 1))
        next_piece = random.choice(pieces)
        logger.info("Generated next piece %s", next_piece)
        can_move_piece = grid.can_move(current_piece, tuple(position), 'b')

        if not can_move_piece:
            logger.info("No more moves available, game over")
            break

        while can_move_piece:
            grid.put_piece(current_piece, tuple(position))
            gui.update_window(grid.matrix, next_piece)

            current_piece = gui.handle_key_events(position, current_piece, next_piece, grid)
            can_move_piece = grid.can_move(current_piece, tuple(position), 'b')
            if can_move_piece:
                grid.remove_piece(current_piece, tuple(position))
                position[0] += 1

        grid.matrix, cleared_lines = grid.clear_filled_lines()

        if cleared_lines > 0:
            can_move_piece = False
            gui.score += cleared_lines
            gui.cleared_lines += cleared_lines
            gui.speed_value += 1
            logger.info("Score updated to %s", gui.score)
            gui.update_window(grid.matrix, next_piece)

        gui.clear_piece(next_piece, (10, ROWS // 2))
        current_piece = next_piece

def setup_curses(stdscr: curses.window):
    """Setup the curses environment."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

def teardown_curses(stdscr: curses.window):
    """Teardown the curses environment."""
    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)


def initialize_game():
    """Initialize the game with the arguments provided by the user."""
    arguments = Arguments()
    arguments.parse_arguments()
    if not os.path.exists(DEFAULT_LOG_DIR):
        os.makedirs(DEFAULT_LOG_DIR)
    if arguments.log_path:
        log_path = os.path.join(DEFAULT_LOG_DIR, arguments.log_path)
        logging.basicConfig(filename=log_path, level=logging.INFO, filemode='w')
    else:
        logging.basicConfig(filename=DEFAULT_LOG_FIL, level=logging.INFO, filemode='w')
    logger.info("Starting the game")
    seed = generate_seed()
    random.seed(arguments.seed if arguments.seed else seed)
    logger.info("Seed set by %s",
                f"user is {arguments.seed}" if arguments.seed else f"system is {seed}")
    width = arguments.width if arguments.width else COLS
    height = arguments.height if arguments.height else ROWS
    logger.info(f"game width: {width}, game height: {height}")

    return arguments, width, height

def main(stdscr: curses.window, arguments, width: int, height: int):
    """The main function that initializes the game."""
    try:
        setup_curses(stdscr)
        pieces_folder = arguments.pieces_folder if arguments.pieces_folder else DEFAULT_PIECES_FOLDER
        game_loop(pieces_folder, arguments.speed, width, height)
    finally:
        teardown_curses(stdscr)
        print("trying here")

try:
    arguments, width, height = initialize_game()
    window: curses.window = curses.initscr()
    curses.wrapper(main, arguments, width, height)
except KeyboardInterrupt:
    logger.info("Game interrupted by user (Ctrl+C)")
    print("Game interrupted by user (Ctrl+C)")
