
"""This module contains the Grid class, which represents the game grid."""

import logging
from dataclasses import dataclass
from pieces import rotate_piece
from constants import COLORS
from pieces import ColoredPiece

logger = logging.getLogger(__name__)

@dataclass
class Block:
    """A class to represent a block in the grid."""
    color: int
    char: str

class Grid:
    """A class to represent the game grid."""
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.matrix = [[Block(COLORS["black"], ' ') for _ in range(width)] for _ in range(height)]

    def put_piece(self, colored_piece: ColoredPiece, position: tuple):
        """Put a piece on the grid at the given position."""
        x, y = position
        piece_height = len(colored_piece.piece)
        piece_width = len(colored_piece.piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if colored_piece.piece[i][j] == 'x':
                    self.matrix[x + i][y + j] = Block(colored_piece.color_value,
                                                      colored_piece.piece[i][j])

    def remove_piece(self, piece: list, position: tuple):
        """Remove a piece from the grid at the given position."""
        x, y = position
        piece_height = len(piece)
        piece_width = len(piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 'x':
                    self.matrix[x + i][y + j] = Block(COLORS["black"], ' ')


    def check_collision(self, piece: list, position: tuple):
        """Check if a piece collides with the grid at the given position."""
        x, y = position
        piece_height = len(piece)
        piece_width = len(piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 'x' and self.matrix[x + i][y + j].char == 'x':
                    return True
        return False

    def can_move(self, colored_piece: ColoredPiece, position: tuple, direction: str):
        """Check if a piece can move in the given direction."""
        x, y = position
        self.remove_piece(colored_piece.piece, position)
        new_piece = ColoredPiece(colored_piece.color_value, [row[:] for row in colored_piece.piece])
        if direction == 'l':
            new_position = (x, y - 1)
        elif direction == 'r':
            new_position = (x, y + 1)
        elif direction == 'u':
            new_position = (x - 1, y)
        elif direction == 'd':
            new_position = (x + 1, y)
        elif direction == 'rot':
            new_position = position
            new_piece.piece = rotate_piece(colored_piece.piece)
        else:
            raise ValueError("Invalid direction. Use 'l', 'r', 'u', 'd', or 'rot'.")
        new_x, new_y = new_position
        piece_height = len(new_piece.piece)
        piece_width = len(new_piece.piece[0])
        grid_height = len(self.matrix)
        grid_width = len(self.matrix[0])
        if (new_x < 0 or new_x + piece_height - 1 >= grid_height or new_y < 0 or
            new_y + piece_width - 1 >= grid_width):
            self.put_piece(colored_piece, position)
            return False

        collision = self.check_collision(new_piece.piece, new_position)
        if not collision:
            self.put_piece(new_piece, position)
        else:
            self.put_piece(colored_piece, position)
        return not collision

    def clear_filled_lines(self):
        """Clear filled lines from the grid."""
        grid_width = len(self.matrix[0])
        new_grid = [row for row in self.matrix if any(block.char == ' ' for block in row)]
        cleared_lines = len(self.matrix) - len(new_grid)
        new_grid = [[Block(COLORS["black"], ' ') for _ in range(grid_width)]
                    for _ in range(cleared_lines)] + new_grid
        if cleared_lines > 0:
            logger.info("Cleared %d completed lines", cleared_lines)
        return new_grid, cleared_lines

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.matrix])
