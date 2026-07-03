
"""This module contains functions to read and manipulate pieces."""

import os

from dataclasses import dataclass
from constants import COLORS

@dataclass
class ColoredPiece:
    """A class to represent a piece with a color."""
    color_value: int
    piece: list

def read_pieces(pieces_folder: str, no_color: bool) -> list:
    """Read the pieces from the given folder, assign a color to each, 
    and return them as a list of tuples."""

    pieces = []

    for index, piece_name in enumerate(os.listdir(pieces_folder)):
        path = os.path.join(pieces_folder, piece_name)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as file:
                piece = [list(line.rstrip('\n')) for line in file]
                color_value = 2 + (index % 7) if not no_color else COLORS["white"]
                pieces.append(ColoredPiece(color_value, piece))

    return pieces

def rotate_piece(piece):
    """Rotate the given piece 90 degrees clockwise."""
    return [list(row) for row in zip(*reversed(piece))]

def str_piece(piece):
    """Convert the given piece to a string."""
    return '\n'.join([''.join(row) for row in piece])

def clone_piece(colored_piece: ColoredPiece) -> ColoredPiece:
    """Return a deep clone of the given ColoredPiece."""
    return ColoredPiece(colored_piece.color_value, [row[:] for row in colored_piece.piece])

