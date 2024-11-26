
"""Module to parse the command line arguments."""

import argparse
import os
from constants import MARGIN

# Get terminal dimensions
TERMIANL_SIZE = os.get_terminal_size()
TERMIANL_WIDTH, TERMIANL_HEIGHT= TERMIANL_SIZE.columns, TERMIANL_SIZE.lines

MIN_WIDTH = 5
MAX_WIDTH = TERMIANL_WIDTH//2 - 2 - MARGIN
MIN_HEIGHT = 10
MAX_HEIGHT = TERMIANL_HEIGHT - 2

def check_width(value: int):
    """Check if the width is between {MIN_WIDTH} and {MAX_WIDTH}."""
    ivalue = int(value)
    if ivalue < MIN_WIDTH or ivalue > MAX_WIDTH:
        raise argparse.ArgumentTypeError(f"Value must be between {MIN_WIDTH} and {MAX_WIDTH}, got {value}")
    return ivalue

def check_height(value):
    """Check if the width is between {MIN_HEIGHT} and {MAX_HEIGHT}."""
    ivalue = int(value)
    if ivalue < MIN_HEIGHT or ivalue > MAX_HEIGHT:
        raise argparse.ArgumentTypeError(f"Value must be between {MIN_HEIGHT} and {MAX_HEIGHT}, got {value}")
    return ivalue

def check_speed(value: str):
    """Check if the speed is one of 'slow', 'medium', 'fast'."""
    if value not in ["slow", "medium", "fast"]:
        raise argparse.ArgumentTypeError("Speed value must be 'slow', 'medium' or 'fast'")
    return value

class Arguments:
    """Class to parse the command line arguments."""
    def __init__(self):
        self.seed = None
        self.log_path = None
        self.pieces_folder = None
        self.speed = None
        self.width = None
        self.height = None

    def parse_arguments(self):
        """Parse the command line arguments."""
        parser = argparse.ArgumentParser(description='Launch Termtris')
        parser.add_argument("--seed", type=int, default=None, help="Seed for the random generator")
        parser.add_argument("--log", type=str , help="Path to the log file")
        parser.add_argument("--piece", "-p", type=str , help="Path to the pieces file")
        parser.add_argument("--speed", "-s", type=check_speed , help="Speed of the game at the start")
        parser.add_argument("--width", "-w", type=check_width , help="Width of the game grid")
        parser.add_argument("--height", "-l", type=check_height , help="Height of the game grid")

        args = parser.parse_args()
        if args.seed:
            self.seed = args.seed

        if args.log:
            self.log_path = args.log

        if args.piece:
            self.pieces_folder = args.piece

        if args.speed:
            self.speed = args.speed

        if args.width:
            self.width = args.width
        
        if args.height:
            self.height = args.height