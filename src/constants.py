"""Module defining the constants of the game"""

import os

COLS = 10
ROWS = 20
MARGIN = 20

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PIECES_FOLDER = os.path.join(CURRENT_PATH, '../pieces')
DEFAULT_LOG_DIR = os.path.join(CURRENT_PATH, '../log/')
DEFAULT_LOG_FIL = os.path.join(CURRENT_PATH, '../log/game.log')

# Get terminal dimensions
try:
    TERMIANL_SIZE = os.get_terminal_size()
    TERMIANL_WIDTH, TERMIANL_HEIGHT = TERMIANL_SIZE.columns, TERMIANL_SIZE.lines
except OSError:
    TERMIANL_WIDTH, TERMIANL_HEIGHT = 80, 24

MIN_WIDTH = 5
MAX_WIDTH = TERMIANL_WIDTH//2 - 2 - MARGIN
MIN_HEIGHT = 10
MAX_HEIGHT = TERMIANL_HEIGHT - 2

PIECE_CHAR = '█'
GHOST_CHAR_1 = '['
GHOST_CHAR_2 = ']'
HORIZONTAL_BORDER = '═'
VERTICAL_BORDER = '║'
T_L_CORNER = '╔'
T_R_CORNER = '╗'
B_L_CORNER = '╚'
B_R_CORNER = '╝'

BASE_WAIT_TIME = 1000
DECREMENT_FACTOR = 0.2

SPEEDS = {
    "slow": 1,
    "medium": 3,
    "fast": 5
}

COLORS = {
    "black": 1, # backgroud
    "blue": 2,
    "cyan": 3,
    "green": 4,
    "magenta": 5,
    "red": 6,
    "white": 7, # instructions
    "yellow": 8 # walls
}
