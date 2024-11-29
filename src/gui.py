"""This module contains the GameWindow class, which represents the game window."""

import logging
import curses
import time
from grid import Grid
from pieces import rotate_piece
from constants import PIECE_CHAR, SPEED_VALUES, BASE_WAIT_TIME, DECREMENT_FACTOR, COLORS
from pieces import ColoredPiece

logger = logging.getLogger(__name__)

class GameWindow:
    """A class to represent the game window."""
    def __init__(self, window: curses.window, margin: int, speed: str):
        self.window = window
        self.margin = margin
        self.score = 0
        self.cleared_lines = 0
        self.speed_value = SPEED_VALUES[speed if speed else "medium"]

    def draw_piece(self, colored_piece: ColoredPiece, start_pos: tuple):
        """Draw a piece on the game window."""
        for y, row in enumerate(colored_piece.piece):
            for x, char in enumerate(row):
                if char == 'x':
                    self.window.addch(start_pos[1] + y, start_pos[0] + x * 2,
                                      PIECE_CHAR, curses.color_pair(colored_piece.color_value))
                    self.window.addch(start_pos[1] + y, start_pos[0] + x * 2 + 1,
                                      PIECE_CHAR, curses.color_pair(colored_piece.color_value))

    def clear_piece(self, colored_piece: ColoredPiece, pos: tuple):
        """Clear a piece from the game window."""
        for y, row in enumerate(colored_piece.piece):
            for x, char in enumerate(row):
                if char == 'x':
                    self.window.addch(pos[1] + y, pos[0] + x * 2, ' ', curses.color_pair(colored_piece.color_value))
                    self.window.addch(pos[1] + y, pos[0] + x * 2 + 1, ' ', curses.color_pair(colored_piece.color_value))

    def draw_grid(self, matrix: list):
        """Draw the game grid on the game window."""
        for y, row in enumerate(matrix):
            for x, block in enumerate(row):
                color_pair = curses.color_pair(block.color)
                character = ' ' if block.char == ' ' else PIECE_CHAR
                self.window.addch(y + 1, x * 2 + self.margin + 1, character, color_pair)
                self.window.addch(y + 1, x * 2 + self.margin + 2, character, color_pair)

    def draw_borders(self, cols: int, rows: int, color):
        """Draw the borders of the game window."""
        horizontal_border = '─'
        vertical_border = '│'
        color_pair = color
        for x in range(cols + 1):
            self.window.addch(0, x * 2 + self.margin, horizontal_border, color_pair)
            self.window.addch(0, x * 2 + 1 + self.margin, horizontal_border, color_pair)
            self.window.addch(rows + 1, x * 2 + self.margin, horizontal_border, color_pair)
            self.window.addch(rows + 1, x * 2 + 1 + self.margin, horizontal_border, color_pair)
        for y in range(rows + 2):
            self.window.addch(y, self.margin, vertical_border, color_pair)
            self.window.addch(y, cols * 2 + 1 + self.margin, vertical_border, color_pair)

    def handle_key_events(self,
                        position: list,
                        current_piece: ColoredPiece,
                        next_piece: ColoredPiece,
                        grid: Grid):
        """Handle key events for moving and rotating the current piece."""
        wait_time = self.compute_wait_time()
        start_time = time.time()
        while time.time() - start_time < wait_time / 1000: # wait_time is in milliseconds
            key = self.window.getch()
            self.window.timeout(wait_time)
            if key == curses.KEY_LEFT and grid.can_move(current_piece, tuple(position), 'l'):
                grid.remove_piece(current_piece.piece, tuple(position))
                position[1] -= 1
                grid.put_piece(current_piece, tuple(position))
                logger.info("Moving piece %s left to position %s", current_piece.piece, position)
            elif key == curses.KEY_RIGHT and grid.can_move(current_piece, tuple(position), 'r'):
                grid.remove_piece(current_piece.piece, tuple(position))
                position[1] += 1
                grid.put_piece(current_piece, tuple(position))
                logger.info("Moving piece %s right to position %s", current_piece.piece, position)
            elif key == ord(' ') and grid.can_move(current_piece, tuple(position), 'rot'):
                grid.remove_piece(current_piece.piece, tuple(position))
                current_piece.piece = rotate_piece(current_piece.piece)
                grid.put_piece(current_piece, tuple(position))
                logger.info("Rotating piece into %s in position %s", current_piece.piece, position)
            elif key == curses.KEY_DOWN:
                logger.info("Moving piece %s down to position %s", current_piece.piece, position)
                break
            self.update_window(grid.matrix, next_piece)
        return current_piece

    def update_window(self, matrix: list, next_piece: ColoredPiece):
        """Update the game window with the current state of the game."""
        self.window.erase()
        self.draw_grid(matrix)
        self.draw_borders(len(matrix[0]), len(matrix), curses.color_pair(COLORS['yellow']))
        start_pos = ((self.margin) // 2 - len(next_piece.piece[0]) // 2, len(matrix) // 2 - 1) #(x, y)
        self.draw_piece(next_piece, start_pos)
        self.display_speed((1, 2))
        self.display_score((2, 2))
        self.display_instructions((1, self.margin + len(matrix[0]) * 2 + 2)) #(y, x)
        self.window.refresh()

    def display_score(self, position: tuple):
        """Display the current score on the game window."""
        score_str = f'score : {self.score}'
        x, y = position
        for i, char in enumerate(score_str):
            self.window.addch(x, y + i, char)

    def compute_wait_time(self) -> int:
        """Compute the wait time based on the current score."""
        wait_time = int(BASE_WAIT_TIME - self.speed_value * DECREMENT_FACTOR * BASE_WAIT_TIME)
        if wait_time <= 0:
            wait_time = int(DECREMENT_FACTOR * BASE_WAIT_TIME)
        return wait_time

    def display_speed(self, position: tuple):
        """Display the current speed on the game window."""
        speed_str = f'speed : {self.speed_value}x'
        x, y = position
        for i, char in enumerate(speed_str):
            self.window.addch(x, y + i, char)

    def display_instructions(self, position: tuple):
        """Display the game instructions on the game window."""
        instructions = [
            "[space] -> rotate",
            "[→] -> move left",
            "[←] -> move right",
            "[↓] -> move down"
        ]
        x, y = position
        for i, instruction in enumerate(instructions):
            for j, char in enumerate(instruction):
                self.window.addch(x + i, y + j, char)
