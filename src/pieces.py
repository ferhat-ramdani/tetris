
"""This module contains functions to read and manipulate pieces."""

import os

def read_pieces(pieces_folder):
    """Read the pieces from the given folder and return them as a list of lists."""
    pieces = []

    for piece_name in os.listdir(pieces_folder):
        path = os.path.join(pieces_folder, piece_name)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as file:
                piece = [list(line.replace('\n', '')) for line in file]
                pieces.append(piece)

    return pieces

def rotate_piece(piece):
    """Rotate the given piece 90 degrees clockwise."""
    return [list(row) for row in zip(*reversed(piece))]

def str_piece(piece):
    """Convert the given piece to a string."""
    return '\n'.join([''.join(row) for row in piece])
