
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
        """Put a piece on the grid at the given position, backing up overwritten cells."""
        x, y = position
        piece_height = len(colored_piece.piece)
        piece_width = len(colored_piece.piece[0])

        if not hasattr(colored_piece, 'overwritten_blocks'):
            colored_piece.overwritten_blocks = {}

        is_ghost_piece = getattr(colored_piece, 'is_ghost', False)
        for i in range(piece_height):
            for j in range(piece_width):
                if colored_piece.piece[i][j] == 'x':
                    grid_r = x + i
                    grid_c = y + j
                    # Save the overwritten block
                    colored_piece.overwritten_blocks[(grid_r, grid_c)] = self.matrix[grid_r][grid_c]
                    # Put active block character ('g' for ghost, 'x' for normal)
                    char_type = 'g' if is_ghost_piece else 'x'
                    self.matrix[grid_r][grid_c] = Block(colored_piece.color_value, char_type)

    def remove_piece(self, colored_piece, position: tuple):
        """Remove a piece from the grid, restoring original cell contents."""
        x, y = position
        if hasattr(colored_piece, 'overwritten_blocks') and colored_piece.overwritten_blocks:
            for (grid_r, grid_c), original_block in colored_piece.overwritten_blocks.items():
                self.matrix[grid_r][grid_c] = original_block
            colored_piece.overwritten_blocks.clear()
        else:
            # Fallback to older list-based remove logic if it's not a ColoredPiece object
            piece_list = colored_piece.piece if hasattr(colored_piece, 'piece') else colored_piece
            piece_height = len(piece_list)
            piece_width = len(piece_list[0])
            for i in range(piece_height):
                for j in range(piece_width):
                    if piece_list[i][j] == 'x':
                        self.matrix[x + i][y + j] = Block(COLORS["black"], ' ')

    def check_collision(self, piece: list, position: tuple):
        """Check if a piece collides with any occupied grid cells at the given position."""
        x, y = position
        piece_height = len(piece)
        piece_width = len(piece[0])

        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 'x' and self.matrix[x + i][y + j].char != ' ':
                    return True
        return False

    def can_move(self, colored_piece: ColoredPiece, position: tuple, direction: str):
        """Check if a piece can move in the given direction."""
        x, y = position
        
        # Check if piece is actually on the grid right now
        was_on_grid = hasattr(colored_piece, 'overwritten_blocks') and bool(colored_piece.overwritten_blocks)
        
        if was_on_grid:
            self.remove_piece(colored_piece, position)
            
        new_piece = ColoredPiece(colored_piece.color_value, [row[:] for row in colored_piece.piece], getattr(colored_piece, 'is_ghost', False))
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
        
        # Check boundary collision
        if (new_x < 0 or new_x + piece_height - 1 >= grid_height or new_y < 0 or
            new_y + piece_width - 1 >= grid_width):
            if was_on_grid:
                self.put_piece(colored_piece, position)
            return False

        # Ghost pieces bypass grid block collision
        is_ghost_piece = getattr(colored_piece, 'is_ghost', False)
        collision = False if is_ghost_piece else self.check_collision(new_piece.piece, new_position)
        
        if was_on_grid:
            self.put_piece(colored_piece, position)
        return not collision

    def finalize_piece(self, colored_piece: ColoredPiece, position: tuple):
        """Solidify the piece into the grid, resolving overwritten blocks for ghost pieces."""
        is_ghost_piece = getattr(colored_piece, 'is_ghost', False)
        if is_ghost_piece and hasattr(colored_piece, 'overwritten_blocks'):
            for (grid_r, grid_c), original_block in colored_piece.overwritten_blocks.items():
                if original_block.char != ' ':
                    self.matrix[grid_r][grid_c] = original_block
                else:
                    self.matrix[grid_r][grid_c].char = 'x'
            colored_piece.overwritten_blocks.clear()
        elif hasattr(colored_piece, 'overwritten_blocks'):
            for (grid_r, grid_c) in list(colored_piece.overwritten_blocks.keys()):
                self.matrix[grid_r][grid_c].char = 'x'
            colored_piece.overwritten_blocks.clear()


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
