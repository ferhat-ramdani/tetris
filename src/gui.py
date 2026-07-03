"""This module contains the GameWindow class, which represents the game window."""

import logging
import curses
import time
from grid import Grid
from pieces import rotate_piece
from constants import PIECE_CHAR, SPEEDS, BASE_WAIT_TIME, DECREMENT_FACTOR, \
    COLORS, HORIZONTAL_BORDER, VERTICAL_BORDER, T_L_CORNER, T_R_CORNER, B_L_CORNER, B_R_CORNER
from pieces import ColoredPiece

logger = logging.getLogger(__name__)

class GameWindow:
    """A class to represent the game window."""
    def __init__(self, window: curses.window, margin: int, speed: str):
        self.window = window
        self.margin = margin
        self.score = 0
        self.cleared_lines = 0
        self.difficulty = speed if speed else "medium"
        self.speed_level = 1
        self.combo_count = 0

    def draw_piece(self, colored_piece: ColoredPiece, start_pos: tuple):
        """Draw a piece on the game window."""
        char_to_draw = '▒' if getattr(colored_piece, 'is_ghost', False) else PIECE_CHAR
        for y, row in enumerate(colored_piece.piece):
            for x, char in enumerate(row):
                if char == 'x':
                    self.window.addch(start_pos[1] + y, start_pos[0] + x * 2,
                                      char_to_draw, curses.color_pair(colored_piece.color_value))
                    self.window.addch(start_pos[1] + y, start_pos[0] + x * 2 + 1,
                                      char_to_draw, curses.color_pair(colored_piece.color_value))

    def clear_piece(self, colored_piece: ColoredPiece, pos: tuple):
        """Clear a piece from the game window."""
        for y, row in enumerate(colored_piece.piece):
            for x, char in enumerate(row):
                if char == 'x':
                    self.window.addch(pos[1] + y, pos[0] + x * 2, ' ', curses.color_pair(colored_piece.color_value))
                    self.window.addch(pos[1] + y, pos[0] + x * 2 + 1, ' ', curses.color_pair(colored_piece.color_value))

    def draw_grid(self, matrix: list):
        """Draw the game grid on the game window, offset by 3 rows for the top panel."""
        for y, row in enumerate(matrix):
            for x, block in enumerate(row):
                color_pair = curses.color_pair(block.color)
                if block.char == ' ':
                    character = ' '
                elif block.char == 'g':
                    character = '▒'
                else:
                    character = PIECE_CHAR
                self.window.addch(y + 3, x * 2 + self.margin + 1, character, color_pair)
                self.window.addch(y + 3, x * 2 + self.margin + 2, character, color_pair)
    
    def draw_borders(self, cols: int, rows: int, color):
        """Draw the borders of the game window, offset by 2 rows for the top panel."""
        color_pair = color
        for x in range(cols+1):
            self.window.addch(2, x * 2 + self.margin, HORIZONTAL_BORDER, color_pair)
            self.window.addch(2, x * 2 + self.margin + 1, HORIZONTAL_BORDER, color_pair)
            self.window.addch(rows + 3, x * 2 + self.margin, HORIZONTAL_BORDER, color_pair)
            self.window.addch(rows + 3, x * 2 + self.margin + 1, HORIZONTAL_BORDER, color_pair)
        for y in range(rows + 2):
            grid_y = y + 2
            if y == 0:
                self.window.addch(grid_y, self.margin, T_L_CORNER, color_pair)
                self.window.addch(grid_y, cols * 2 + 1 + self.margin, T_R_CORNER, color_pair)
            elif y == rows + 1:
                self.window.addch(grid_y, self.margin, B_L_CORNER, color_pair)
                self.window.addch(grid_y, cols * 2 + 1 + self.margin, B_R_CORNER, color_pair)
            else:
                self.window.addch(grid_y, self.margin, VERTICAL_BORDER, color_pair)
                self.window.addch(grid_y, cols * 2 + 1 + self.margin, VERTICAL_BORDER, color_pair)

    def draw_shadow(self, colored_piece: ColoredPiece, shadow_pos: tuple, matrix: list):
        """Draw the shadow preview of the piece at its projected landing row."""
        shadow_r, shadow_c = shadow_pos
        shadow_char = '░'
        # Use a faint color for the shadow so it doesn't look like an actual block
        color_pair = curses.color_pair(COLORS["white"]) | curses.A_DIM
        for y, row in enumerate(colored_piece.piece):
            for x, char in enumerate(row):
                if char == 'x':
                    grid_r = shadow_r + y
                    grid_c = shadow_c + x
                    if 0 <= grid_r < len(matrix) and 0 <= grid_c < len(matrix[0]):
                        if matrix[grid_r][grid_c].char == ' ':
                            scr_y = grid_r + 3
                            scr_x1 = grid_c * 2 + self.margin + 1
                            scr_x2 = grid_c * 2 + self.margin + 2
                            self.window.addch(scr_y, scr_x1, shadow_char, color_pair)
                            self.window.addch(scr_y, scr_x2, shadow_char, color_pair)

    def handle_key_events(self,
                        position: list,
                        current_piece: ColoredPiece,
                        next_piece: ColoredPiece,
                        grid: Grid,
                        shadow_pos: tuple = None,
                        ai_mode: bool = False,
                        target_rot: int = 0,
                        target_col: int = 0):
        """Handle key events for moving and rotating the current piece (supports AI playback)."""
        wait_time = self.compute_wait_time()
        start_time = time.time()
        
        if ai_mode:
            # AI step-by-step solver simulation loop
            self.window.nodelay(True)
            while time.time() - start_time < wait_time / 1000:
                user_key = self.window.getch()
                if user_key in [ord('m'), ord('q'), ord('M'), ord('Q'), 27]:
                    return "MENU"
                    
                key = None
                curr_rot = getattr(current_piece, 'rot_count', 0)
                if curr_rot < target_rot:
                    key = ord(' ')
                elif position[1] < target_col:
                    key = curses.KEY_RIGHT
                elif position[1] > target_col:
                    key = curses.KEY_LEFT
                else:
                    # Aligned! Drop immediately
                    time.sleep(0.02) # Very small delay so it's smooth
                    break
                
                # Execute simulated AI key stroke
                if key == ord(' ') and grid.can_move(current_piece, tuple(position), 'rot'):
                    grid.remove_piece(current_piece, tuple(position))
                    current_piece.piece = rotate_piece(current_piece.piece)
                    current_piece.rot_count = curr_rot + 1
                    grid.put_piece(current_piece, tuple(position))
                elif key == curses.KEY_LEFT and grid.can_move(current_piece, tuple(position), 'l'):
                    grid.remove_piece(current_piece, tuple(position))
                    position[1] -= 1
                    grid.put_piece(current_piece, tuple(position))
                elif key == curses.KEY_RIGHT and grid.can_move(current_piece, tuple(position), 'r'):
                    grid.remove_piece(current_piece, tuple(position))
                    position[1] += 1
                    grid.put_piece(current_piece, tuple(position))
                
                # Update shadow position
                if shadow_pos is not None:
                    x_c, y_c = position
                    grid.remove_piece(current_piece, position)
                    s_r = x_c
                    p_h = len(current_piece.piece)
                    while s_r + p_h < grid.height:
                        if grid.check_collision(current_piece.piece, (s_r + 1, y_c)):
                            break
                        s_r += 1
                    grid.put_piece(current_piece, position)
                    shadow_pos = (s_r, y_c)
                
                self.update_window(grid.matrix, next_piece, shadow_pos, current_piece)
                time.sleep(0.08) # 80ms animation delay between AI operations
            return current_piece
            
        # Normal player keyboard handling
        while time.time() - start_time < wait_time / 1000:
            key = self.window.getch()
            self.window.timeout(wait_time)
            
            if key in [ord('m'), ord('q'), ord('M'), ord('Q'), 27]:
                return "MENU"
                
            if key == curses.KEY_LEFT and grid.can_move(current_piece, tuple(position), 'l'):
                grid.remove_piece(current_piece, tuple(position))
                position[1] -= 1
                grid.put_piece(current_piece, tuple(position))
                logger.info("Moving piece left to position %s", position)
            elif key == curses.KEY_RIGHT and grid.can_move(current_piece, tuple(position), 'r'):
                grid.remove_piece(current_piece, tuple(position))
                position[1] += 1
                grid.put_piece(current_piece, tuple(position))
                logger.info("Moving piece right to position %s", position)
            elif key == ord(' ') and grid.can_move(current_piece, tuple(position), 'rot'):
                grid.remove_piece(current_piece, tuple(position))
                current_piece.piece = rotate_piece(current_piece.piece)
                grid.put_piece(current_piece, tuple(position))
                logger.info("Rotating piece into %s in position %s", current_piece.piece, position)
            elif key == curses.KEY_DOWN:
                logger.info("Moving piece down to position %s", position)
                break
            elif key == curses.KEY_UP:
                if getattr(current_piece, 'is_ghost', False):
                    # For ghost pieces, instantly solidify in place
                    return "SOLIDIFY"
                else:
                    # For normal pieces, Hard Drop to shadow position
                    if shadow_pos is not None:
                        grid.remove_piece(current_piece, tuple(position))
                        position[0] = shadow_pos[0]
                        grid.put_piece(current_piece, tuple(position))
                        logger.info("Hard dropped piece to position %s", position)
                        return "SOLIDIFY"
            if key:
                if shadow_pos is not None:
                    x_c, y_c = position
                    grid.remove_piece(current_piece, position)
                    s_r = x_c
                    p_h = len(current_piece.piece)
                    while s_r + p_h < grid.height:
                        if grid.check_collision(current_piece.piece, (s_r + 1, y_c)):
                            break
                        s_r += 1
                    grid.put_piece(current_piece, position)
                    shadow_pos = (s_r, y_c)
                self.update_window(grid.matrix, next_piece, shadow_pos, current_piece)
        return current_piece

    def update_window(self, matrix: list, next_piece: ColoredPiece, shadow_pos: tuple = None, current_piece: ColoredPiece = None):
        """Update the game window with the current state of the game."""
        self.window.erase()
        
        # Draw the grid BEFORE the shadow so the shadow overwrites empty spaces
        self.draw_grid(matrix)
        
        # Draw shadow over grid
        if shadow_pos is not None and current_piece is not None:
            self.draw_shadow(current_piece, shadow_pos, matrix)
            
        self.draw_borders(len(matrix[0]), len(matrix), curses.color_pair(COLORS['yellow']))
        
        # Draw next piece preview (placed at left margin space)
        x = (self.margin) // 2 - len(next_piece.piece[0])
        y = len(matrix) // 2 + 1
        self.draw_piece(next_piece, (x, y))
        
        # Display top headers and bottom footers
        self.display_top_header(len(matrix[0]))
        self.display_instructions(len(matrix), len(matrix[0]))
        self.window.refresh()

    def display_top_header(self, cols_count: int):
        """Display Score and Speed side-by-side in the top panel."""
        score_str = f"SCORE: {self.score:<6}"
        speed_str = f"SPEED: {self.speed_level}x ({self.difficulty})"
        
        # Draw top panel text
        self.window.addstr(0, 2, score_str, curses.A_BOLD)
        right_offset = self.margin + cols_count * 2 - len(speed_str)
        self.window.addstr(0, max(2, right_offset), speed_str, curses.A_BOLD)
        
        # Draw horizontal dividing double line below the text
        div_line = "═" * (self.margin + cols_count * 2 + 4)
        self.window.addstr(1, 0, div_line)

    def compute_wait_time(self) -> int:
        """Compute the wait time based on the active difficulty and speed level."""
        base_delays = {"slow": 1000, "medium": 800, "fast": 500}
        decay_factors = {"slow": 0.9, "medium": 0.85, "fast": 0.8}
        
        base = base_delays.get(self.difficulty, 800)
        decay = decay_factors.get(self.difficulty, 0.85)
        
        wait_time = int(base * (decay ** (self.speed_level - 1)))
        return max(50, wait_time)

    def display_instructions(self, rows_count: int, cols_count: int):
        """Display the game instructions centered at the bottom panel in a 3x2 grid."""
        total_width = self.margin + cols_count * 2 + 2
        y_pos = rows_count + 4
        
        r1 = f"{'[←] Left':^14} │ {'[→] Right':^14} │ {'[↓] Down':^14}"
        r2 = f"{'[SPC] Rotate':^14} │ {'[M] Menu':^14} │ {'[↑] Drop/Fix':^14}"
        
        x_pos1 = (total_width - len(r1)) // 2
        x_pos2 = (total_width - len(r2)) // 2
        
        self.window.addstr(y_pos, max(0, x_pos1), r1, curses.A_DIM)
        self.window.addstr(y_pos + 1, max(0, x_pos2), r2, curses.A_DIM)
