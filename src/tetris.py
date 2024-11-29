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
from constants import COLS, ROWS, MARGIN, DEFAULT_PIECES_FOLDER, DEFAULT_LOG_DIR, DEFAULT_LOG_FIL, COLORS

logger = logging.getLogger(__name__)

def game_loop(pieces_folder: str,
              speed: str,
              width: int,
              height: int
              ):
    """The main game loop that runs until the game is over."""
    colored_pieces = read_pieces(pieces_folder)
    grid = Grid(height, width)
    gui = GameWindow(window, MARGIN, speed)

    current_colored_piece = random.choice(colored_pieces)
    logger.info("Generated piece %s", current_colored_piece)

    while True:
        position = list((0, width // 2 - 1))
        next_colored_piece = random.choice(colored_pieces)
        logger.info("Generated next piece %s", next_colored_piece)
        can_move_piece = grid.can_move(current_colored_piece, tuple(position), 'd')

        if not can_move_piece:
            logger.info("No more moves available, game over")
            break

        while can_move_piece:
            grid.put_piece(current_colored_piece, tuple(position))
            gui.update_window(grid.matrix, next_colored_piece)

            current_colored_piece = gui.handle_key_events(position, current_colored_piece, next_colored_piece, grid)
            can_move_piece = grid.can_move(current_colored_piece, tuple(position), 'd')
            if can_move_piece:
                grid.remove_piece(current_colored_piece.piece, tuple(position))
                position[0] += 1

        grid.matrix, cleared_lines = grid.clear_filled_lines()

        if cleared_lines > 0:
            can_move_piece = False
            gui.score += cleared_lines
            gui.cleared_lines += cleared_lines
            gui.speed_value += 1
            logger.info("Score updated to %s", gui.score)
            gui.update_window(grid.matrix, next_colored_piece)

        gui.clear_piece(next_colored_piece, (10, ROWS // 2)) # what does that do?
        current_colored_piece = next_colored_piece

def setup_curses(stdscr: curses.window):
    """Setup the curses environment."""
    curses.start_color()
    for color_name, pair_number in COLORS.items():
        curses.init_pair(pair_number, getattr(curses, f"COLOR_{color_name.upper()}"),
                         curses.COLOR_BLACK)
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
        logging.basicConfig(filename=log_path,
                            level=logging.INFO,
                            filemode='w')
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
        pieces_folder = arguments.pieces_folder if arguments.pieces_folder \
            else DEFAULT_PIECES_FOLDER
        game_loop(pieces_folder, arguments.speed, width, height)
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e
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
