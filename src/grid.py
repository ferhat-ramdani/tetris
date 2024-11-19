
"""This module contains the Grid class, which represents the game grid."""

import logging
from typing import List
from pieces import rotate_piece

logger = logging.getLogger(__name__)

class Grid:
    """A class to represent the game grid."""
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.matrix = [[' ' for _ in range(width)] for _ in range(height)]

    def put_piece(self, piece: List[List[str]], position: tuple[int, int]):
        """Put a piece on the grid at the given position."""
        x, y = position
        piece_height = len(piece)
        piece_width = len(piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 'x':
                    self.matrix[x + i][y + j] = piece[i][j]

    def remove_piece(self, piece: List[List[str]], position: tuple[int, int]):
        """Remove a piece from the grid at the given position."""
        x, y = position
        piece_height = len(piece)
        piece_width = len(piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 'x':
                    self.matrix[x + i][y + j] = ' '


    def check_collision(self, piece: List[List[str]], position: tuple[int, int]):
        """Check if a piece collides with the grid at the given position."""
        x, y = position
        piece_height = len(piece)
        piece_width = len(piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 'x' and self.matrix[x + i][y + j] == 'x':
                    return True
        return False

    def can_move(self, piece: List[List[str]], position: tuple[int, int], direction: str):
        """Check if a piece can move in the given direction."""
        x, y = position
        self.remove_piece(piece, position)
        new_piece = piece
        if direction == 'l':
            new_position = (x, y - 1)
        elif direction == 'r':
            new_position = (x, y + 1)
        elif direction == 'u':
            new_position = (x - 1, y)
        elif direction == 'b':
            new_position = (x + 1, y)
        elif direction == 'rot':
            new_position = position
            new_piece = rotate_piece(piece)
        else:
            raise ValueError("Invalid direction. Use 'l', 'r', 'u', 'b', or 'rot'.")
        new_x, new_y = new_position
        piece_height = len(new_piece)
        piece_width = len(new_piece[0])
        grid_height = len(self.matrix)
        grid_width = len(self.matrix[0])
        if (new_x < 0 or new_x + piece_height - 1 >= grid_height or new_y < 0 or
            new_y + piece_width - 1 >= grid_width):
            self.put_piece(piece, position)
            return False

        collision = self.check_collision(new_piece, new_position)
        if not collision:
            self.put_piece(new_piece, position)
        else:
            self.put_piece(piece, position)
        return not collision

    def clear_filled_lines(self):
        """Clear filled lines from the grid."""
        grid_width = len(self.matrix[0])
        new_grid = [row for row in self.matrix if row.count('x') != grid_width]
        lines_cleared = len(self.matrix) - len(new_grid)
        new_grid = [[' ' for _ in range(grid_width)] for _ in range(lines_cleared)] + new_grid
        logger.info("Cleared %d completed lines", lines_cleared)
        return new_grid, lines_cleared

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.matrix])
