
"""This module contains the GameWindow class, which represents the game window."""

import logging
import curses
import time
from typing import List, Tuple
from grid import Grid
from pieces import rotate_piece

logger = logging.getLogger(__name__)

PIECE_CHAR = '█'
BASE_WAIT_TIME = 100
DECREMENT_FACTOR = 0.1

class GameWindow:
    """A class to represent the game window."""
    def __init__(self, window: curses.window, margin: int, log_set: bool):
        self.window = window
        self.margin = margin
        self.score = 0
        self.log_set = log_set

    def draw_piece(self, piece: List[List[str]], start_pos: Tuple[int, int]):
        """Draw a piece on the game window."""
        for y, row in enumerate(piece):
            for x, char in enumerate(row):
                if char == 'x':
                    self.window.addch(start_pos[1] + y, start_pos[0] + x * 2, PIECE_CHAR)
                    self.window.addch(start_pos[1] + y, start_pos[0] + x * 2 + 1, PIECE_CHAR)

    def clear_piece(self, piece: List[List[str]], pos: Tuple[int, int]):
        """Clear a piece from the game window."""
        for y, row in enumerate(piece):
            for x, char in enumerate(row):
                if char == 'x':
                    self.window.addch(pos[1] + y, pos[0] + x * 2, ' ')
                    self.window.addch(pos[1] + y, pos[0] + x * 2 + 1, ' ')

    def draw_grid(self, matrix: List[List[str]]):
        """Draw the game grid on the game window."""
        for y, row in enumerate(matrix):
            for x, char in enumerate(row):
                character = PIECE_CHAR if char == 'x' else ' '
                self.window.addch(y + 1, x * 2 + self.margin + 1, character)
                self.window.addch(y + 1, x * 2 + self.margin + 2, character)

    def draw_borders(self, cols: int, rows: int):
        """Draw the borders of the game window."""
        horizontal_border = '─'
        vertical_border = '│'
        for x in range(cols + 1):
            self.window.addch(0, x * 2 + self.margin, horizontal_border)
            self.window.addch(0, x * 2 + 1 + self.margin, horizontal_border)
            self.window.addch(rows + 1, x * 2 + self.margin, horizontal_border)
            self.window.addch(rows + 1, x * 2 + 1 + self.margin, horizontal_border)
        for y in range(rows + 2):
            self.window.addch(y, self.margin, vertical_border)
            self.window.addch(y, cols * 2 + 1 + self.margin, vertical_border)

    def handle_key_events(self, position: List[int], current_piece: List[List[str]], next_piece: List[List[str]], grid: Grid):
        """Handle key events for moving and rotating the current piece."""
        wait_time = self.compute_wait_time()
        start_time = time.time()
        while time.time() - start_time < wait_time / 1000:
            key = self.window.getch()
            self.window.timeout(wait_time)
            if key == curses.KEY_LEFT and grid.can_move(current_piece, tuple(position), 'l'):
                grid.remove_piece(current_piece, tuple(position))
                position[1] -= 1
                grid.put_piece(current_piece, tuple(position))
                if self.log_set:
                    logger.info("Moving piece %s left to position %s", current_piece, position)
            elif key == curses.KEY_RIGHT and grid.can_move(current_piece, tuple(position), 'r'):
                grid.remove_piece(current_piece, tuple(position))
                position[1] += 1
                grid.put_piece(current_piece, tuple(position))
                if self.log_set:
                    logger.info("Moving piece %s right to position %s", current_piece, position)
            elif key == ord(' ') and grid.can_move(current_piece, tuple(position), 'rot'):
                grid.remove_piece(current_piece, tuple(position))
                current_piece = rotate_piece(current_piece)
                grid.put_piece(current_piece, tuple(position))
                if self.log_set:
                    logger.info("Rotating piece into %s in position %s", current_piece, position)
            elif key == curses.KEY_DOWN:
                if self.log_set:
                    logger.info("Moving piece %s down to position %s", current_piece, position)
                break
            grid.matrix = grid.clear_filled_lines()[0]
            self.window.clear()
            self.update_window(grid.matrix, next_piece)
            self.window.refresh()
        return current_piece

    def update_window(self, matrix: List[List[str]], next_piece: List[List[str]]):
        """Update the game window with the current state of the game."""
        self.draw_grid(matrix)
        self.draw_borders(len(matrix[0]), len(matrix))
        start_pos = (len(matrix[0]) // 2 - 3, 7)
        self.draw_piece(next_piece, start_pos)
        self.display_wait_time((1, 2))
        self.display_score((2, 2))
        self.window.refresh()

    def display_score(self, position: Tuple[int, int]):
        """Display the current score on the game window."""
        score_str = f'score : {self.score}'
        x, y = position
        for i, char in enumerate(score_str):
            self.window.addch(x, y + i, char)

    def compute_wait_time(self) -> int:
        """Compute the wait time based on the current score."""
        return int (BASE_WAIT_TIME - self.score * DECREMENT_FACTOR * BASE_WAIT_TIME)

    def display_wait_time(self, position: Tuple[int, int]):
        """Display the current speed on the game window."""
        speed_str = f'wait time : {self.compute_wait_time()/1000}s'
        x, y = position
        for i, char in enumerate(speed_str):
            self.window.addch(x, y + i, char)
