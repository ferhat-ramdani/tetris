
"""Module to parse the command line arguments."""

import argparse
from constants import MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT


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

def parse_arguments():
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description='Launch Termtris')
    parser.add_argument("--seed", type=int, default=None, help="Seed for the random generator")
    parser.add_argument("--log", type=str , help="Path to the log file")
    parser.add_argument("--piece", "-p", type=str , help="Path to the pieces file")
    parser.add_argument("--speed", "-s", type=check_speed , help="Speed of the game at the start, allowed values are 'slow', 'medium' and 'fast'")
    parser.add_argument("--width", "-w", type=check_width , help="Width of the game grid")
    parser.add_argument("--height", "-l", type=check_height , help="Height of the game grid")
    parser.add_argument("--no-color", action='store_true', help="Disable colors in the game")
    parser.add_argument("--no-shadow", action='store_true', help="Disable the landing shadow preview")
    parser.add_argument("--auto", nargs='?', const='PierreDellacherie', default=None, help="Activate AI player mode")
    parser.add_argument("--ghost", action='store_true', help="Enable phasing ghost pieces")

    return parser.parse_args()
