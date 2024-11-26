"""Module defining the constants of the game"""

import os

COLS = 10
ROWS = 20
MARGIN = 20

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PIECES_FOLDER = os.path.join(CURRENT_PATH, '../pieces')
DEFAULT_LOG_DIR = os.path.join(CURRENT_PATH, '../log/')
DEFAULT_LOG_FIL = os.path.join(CURRENT_PATH, '../log/game.log')
