
"""This module contains utility functions for the Tetris game."""

import time

def generate_seed():
    """Generate a seed for the random number generator."""
    return int(time.time())