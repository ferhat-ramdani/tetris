"""The main module that runs the game."""

import curses
import random
import logging
import os

from argparser import parse_arguments
from pieces import read_pieces, clone_piece
from gui import GameWindow
from grid import Grid
from utils import generate_seed
from ai import get_best_move
from constants import COLS, ROWS, MARGIN, DEFAULT_PIECES_FOLDER, DEFAULT_LOG_DIR, DEFAULT_LOG_FIL, COLORS, \
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT, HORIZONTAL_BORDER, VERTICAL_BORDER, T_L_CORNER, T_R_CORNER, \
    B_L_CORNER, B_R_CORNER

logger = logging.getLogger(__name__)


class MenuController:
    def __init__(self, stdscr, arguments):
        self.stdscr = stdscr
        self.default_settings = {
            "speed": arguments.speed if arguments.speed else "medium",
            "width": arguments.width if arguments.width else COLS,
            "height": arguments.height if arguments.height else ROWS,
            "no_color": arguments.no_color,
            "seed": arguments.seed,
            "piece": arguments.piece if arguments.piece else DEFAULT_PIECES_FOLDER,
            "log": arguments.log,
            "mode": "AI" if arguments.auto is not None else "Player",
            "shadow": False if arguments.no_shadow else True,
            "ghost": True if arguments.ghost else False
        }
        self.settings = self.default_settings.copy()
        self.current_menu = "main"
        self.selected_idx = 0
        
        self.main_options = [
            "Start Game (Default Options)",
            "Advanced Options"
        ]
        self.adv_keys = ["speed", "width", "height", "no_color", "mode", "shadow", "ghost", "start", "back"]
        self.adv_labels = [
            "Speed", "Width", "Height", "Disable Colors", 
            "Play Mode", "Shadow Preview", "Ghost Pieces", "Start Game", "Back"
        ]

    def draw_box(self, box_w, box_h):
        h, w = self.stdscr.getmaxyx()
        start_y = (h - box_h) // 2
        start_x = (w - box_w) // 2

        for x_coord in range(start_x, start_x + box_w):
            self.stdscr.addch(start_y, x_coord, HORIZONTAL_BORDER)
            self.stdscr.addch(start_y + box_h - 1, x_coord, HORIZONTAL_BORDER)
        for y_coord in range(start_y, start_y + box_h):
            self.stdscr.addch(y_coord, start_x, VERTICAL_BORDER)
            self.stdscr.addch(y_coord, start_x + box_w - 1, VERTICAL_BORDER)
        self.stdscr.addch(start_y, start_x, T_L_CORNER)
        self.stdscr.addch(start_y, start_x + box_w - 1, T_R_CORNER)
        self.stdscr.addch(start_y + box_h - 1, start_x, B_L_CORNER)
        self.stdscr.addch(start_y + box_h - 1, start_x + box_w - 1, B_R_CORNER)

        title = " TERMTRIS "
        self.stdscr.addstr(start_y, start_x + (box_w - len(title)) // 2, title, curses.A_BOLD)
        return start_y, start_x

    def render_main_menu(self, start_y, start_x, box_w, box_h):
        for idx, opt in enumerate(self.main_options):
            y_pos = start_y + 3 + idx * 2
            x_pos = start_x + 6
            style = curses.A_REVERSE | curses.A_BOLD if idx == self.selected_idx else curses.A_NORMAL
            self.stdscr.addstr(y_pos, x_pos, f"> {opt}" if idx == self.selected_idx else f"  {opt}", style)
        
        help_str = "Use UP/DOWN to navigate, ENTER to select"
        self.stdscr.addstr(start_y + box_h - 2, start_x + (box_w - len(help_str)) // 2, help_str, curses.A_DIM)

    def render_advanced_menu(self, start_y, start_x, box_w, box_h, max_w_val, max_h_val):
        self.settings["width"] = max(MIN_WIDTH, min(self.settings["width"], max_w_val))
        self.settings["height"] = max(MIN_HEIGHT, min(self.settings["height"], max_h_val))

        for idx, key in enumerate(self.adv_keys):
            y_pos = start_y + 2 + idx
            x_pos = start_x + 4
            style = curses.A_REVERSE | curses.A_BOLD if idx == self.selected_idx else curses.A_NORMAL
            
            if key in ["start", "back"]:
                label = f"[ {self.adv_labels[idx]} ]"
                self.stdscr.addstr(y_pos, start_x + (box_w - len(label)) // 2, label, style)
            else:
                val = self.settings[key]
                val_str = "Disabled" if key == "no_color" and val else "Enabled" if key == "no_color" else \
                          "Enabled" if key in ["shadow", "ghost"] and val else "Disabled" if key in ["shadow", "ghost"] else \
                          str(val)
                
                option_line = f"  {self.adv_labels[idx] + ':' :<18} [ {val_str} ]"
                self.stdscr.addstr(y_pos, x_pos, option_line, style)

        help_str = "LEFT/RIGHT to adjust, ENTER to edit/select"
        self.stdscr.addstr(start_y + box_h - 2, start_x + (box_w - len(help_str)) // 2, help_str, curses.A_DIM)

    def handle_main_input(self, key):
        if key == curses.KEY_UP:
            self.selected_idx = (self.selected_idx - 1) % len(self.main_options)
        elif key == curses.KEY_DOWN:
            self.selected_idx = (self.selected_idx + 1) % len(self.main_options)
        elif key in [10, 13]:
            if self.selected_idx == 0:
                return "START_DEFAULT"
            self.current_menu = "advanced"
            self.selected_idx = 0
        return None

    def handle_advanced_input(self, key, max_w_val, max_h_val):
        if key == curses.KEY_UP:
            self.selected_idx = (self.selected_idx - 1) % len(self.adv_keys)
            return None
        if key == curses.KEY_DOWN:
            self.selected_idx = (self.selected_idx + 1) % len(self.adv_keys)
            return None

        current_key = self.adv_keys[self.selected_idx]
        
        # Dispatch table handling individual setting modifications cleanly
        adjustments = {
            "speed": lambda k: self._toggle_speed(k),
            "width": lambda k: self._scale_setting("width", k, MIN_WIDTH, max_w_val),
            "height": lambda k: self._scale_setting("height", k, MIN_HEIGHT, max_h_val),
            "no_color": lambda k: self._toggle_bool("no_color", k),
            "shadow": lambda k: self._toggle_bool("shadow", k),
            "ghost": lambda k: self._toggle_bool("ghost", k),
            "mode": lambda k: self._toggle_mode(k),
            "start": lambda k: "START" if k in [10, 13] else None,
            "back": lambda k: self._go_back(k)
        }
        
        if current_key in adjustments:
            return adjustments[current_key](key)
        return None

    def _toggle_speed(self, key):
        speeds = ["slow", "medium", "fast"]
        idx = speeds.index(self.settings["speed"])
        if key == curses.KEY_LEFT:
            self.settings["speed"] = speeds[(idx - 1) % 3]
        elif key == curses.KEY_RIGHT:
            self.settings["speed"] = speeds[(idx + 1) % 3]

    def _scale_setting(self, key, key_input, min_v, max_v):
        if key_input == curses.KEY_LEFT:
            self.settings[key] = max(min_v, self.settings[key] - 1)
        elif key_input == curses.KEY_RIGHT:
            self.settings[key] = min(max_v, self.settings[key] + 1)

    def _toggle_bool(self, key, key_input):
        if key_input in [curses.KEY_LEFT, curses.KEY_RIGHT, 10, 13]:
            self.settings[key] = not self.settings[key]

    def _toggle_mode(self, key_input):
        if key_input in [curses.KEY_LEFT, curses.KEY_RIGHT, 10, 13]:
            self.settings["mode"] = "AI" if self.settings["mode"] == "Player" else "Player"

    def _go_back(self, key_input):
        if key_input in [10, 13]:
            self.current_menu = "main"
            self.selected_idx = 1
        return None

    def navigate(self):
        self.stdscr.nodelay(False)
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            
            if w < 54 or h < 13:
                self.stdscr.addstr(h // 2, max(0, (w - 22) // 2), "Screen is too small!")
                self.stdscr.refresh()
                self.stdscr.getch()
                continue

            box_w, box_h = 52, (11 if self.current_menu == "main" else 13)
            start_y, start_x = self.draw_box(box_w, box_h)
            
            max_w_val = w // 2 - 16
            max_h_val = h - 8

            if self.current_menu == "main":
                self.render_main_menu(start_y, start_x, box_w, box_h)
                action = self.handle_main_input(self.stdscr.getch())
            else:
                self.render_advanced_menu(start_y, start_x, box_w, box_h, max_w_val, max_h_val)
                action = self.handle_advanced_input(self.stdscr.getch(), max_w_val, max_h_val)

            if action == "START_DEFAULT":
                return self.default_settings
            elif action == "START":
                return self.settings


def compute_shadow(grid: Grid, piece, pos: tuple) -> tuple:
    r, c = pos
    was_on_grid = hasattr(piece, 'overwritten_blocks') and bool(piece.overwritten_blocks)
    if was_on_grid:
        grid.remove_piece(piece, pos)
    shadow_r = r
    p_h = len(piece.piece)
    while shadow_r + p_h < grid.height:
        if grid.check_collision(piece.piece, (shadow_r + 1, c)):
            break
        shadow_r += 1
    if was_on_grid:
        grid.put_piece(piece, pos)
    return (shadow_r, c)

def make_piece(colored_pieces: list, ghost_enabled: bool):
    piece = clone_piece(random.choice(colored_pieces))
    piece.rot_count = 0
    if ghost_enabled and random.random() < 0.15:
        piece.is_ghost = True
        piece.color_value = COLORS.get("cyan", 3)
    return piece

def game_loop(sub_win, pieces_folder, speed_level_str, width, height, no_color, mode, shadow, ghost):
    colored_pieces = read_pieces(pieces_folder, no_color)
    if not colored_pieces:
        logger.error("No pieces loaded. Exiting game loop.")
        return

    grid = Grid(height, width)
    gui = GameWindow(sub_win, 14, speed_level_str)
    
    current_colored_piece = make_piece(colored_pieces, ghost)
    next_colored_piece = make_piece(colored_pieces, ghost)
    gui.update_window(grid.matrix, next_colored_piece, current_piece=current_colored_piece)

    while True:
        position = list((0, width // 2 - 1))
        can_move_piece = True
        if not getattr(current_colored_piece, 'is_ghost', False):
            can_move_piece = grid.can_move(current_colored_piece, tuple(position), 'd')

        if not can_move_piece:
            logger.info("No more moves available, game over")
            break

        gui.clear_piece(next_colored_piece, (10, height // 2))

        ai_t_rot, ai_t_col = 0, 0
        if mode == "AI":
            ai_t_rot, ai_t_col = get_best_move(grid, current_colored_piece)

        while can_move_piece:
            grid.put_piece(current_colored_piece, tuple(position))
            show_shadow = shadow and not getattr(current_colored_piece, 'is_ghost', False)
            shadow_pos = compute_shadow(grid, current_colored_piece, tuple(position)) if show_shadow else None
            gui.update_window(grid.matrix, next_colored_piece, shadow_pos, current_colored_piece)
            
            ret_action = gui.handle_key_events(
                position, current_colored_piece, next_colored_piece, grid, shadow_pos,
                ai_mode=(mode == "AI"), target_rot=ai_t_rot, target_col=ai_t_col
            )
            if ret_action == "MENU":
                return "MENU"
            if ret_action == "SOLIDIFY":
                break
                
            current_colored_piece = ret_action
            can_move_piece = grid.can_move(current_colored_piece, tuple(position), 'd')
            if can_move_piece:
                grid.remove_piece(current_colored_piece, tuple(position))
                position[0] += 1

        grid.finalize_piece(current_colored_piece, tuple(position))
        grid.matrix, cleared_lines = grid.clear_filled_lines()

        if cleared_lines > 0:
            can_move_piece = False
            base_scores = {1: 100, 2: 300, 3: 600, 4: 1000}
            lines_score = base_scores.get(cleared_lines, cleared_lines * 100)
            combo_bonus = 50 * gui.combo_count
            gui.combo_count += 1
            gui.score += lines_score + combo_bonus
            gui.cleared_lines += cleared_lines
            gui.speed_level = 1 + gui.cleared_lines // 5
            
            show_shadow_next = shadow and not getattr(next_colored_piece, 'is_ghost', False)
            shadow_pos_next = compute_shadow(grid, next_colored_piece, (0, width // 2 - 1)) if show_shadow_next else None
            gui.update_window(grid.matrix, next_colored_piece, shadow_pos_next, next_colored_piece)
        else:
            gui.combo_count = 0

        current_colored_piece = next_colored_piece
        next_colored_piece = make_piece(colored_pieces, ghost)

def setup_curses(stdscr):
    curses.start_color()
    for color_name, pair_number in COLORS.items():
        curses.init_pair(pair_number, getattr(curses, f"COLOR_{color_name.upper()}"), curses.COLOR_BLACK)
    stdscr.clear()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

def teardown_curses(stdscr):
    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)

def configure_game(settings):
    if not os.path.exists(DEFAULT_LOG_DIR):
        os.makedirs(DEFAULT_LOG_DIR)
    
    log_file = settings["log"]
    log_path = os.path.join(DEFAULT_LOG_DIR, log_file) if log_file and not os.path.isabs(log_file) else log_file or DEFAULT_LOG_FIL
        
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(filename=log_path, level=logging.INFO, filemode='w')
    seed = generate_seed()
    random.seed(settings["seed"] if settings["seed"] is not None else seed)

def show_game_over(stdscr):
    stdscr.nodelay(False)
    h, w = stdscr.getmaxyx()
    box_w, box_h = 30, 7
    start_y = (h - box_h) // 2
    start_x = (w - box_w) // 2
    
    for x in range(start_x, start_x + box_w):
        stdscr.addch(start_y, x, HORIZONTAL_BORDER)
        stdscr.addch(start_y + box_h - 1, x, HORIZONTAL_BORDER)
    for y in range(start_y, start_y + box_h):
        stdscr.addch(y, start_x, VERTICAL_BORDER)
        stdscr.addch(y, start_x + box_w - 1, VERTICAL_BORDER)
    stdscr.addch(start_y, start_x, T_L_CORNER)
    stdscr.addch(start_y, start_x + box_w - 1, T_R_CORNER)
    stdscr.addch(start_y + box_h - 1, start_x, B_L_CORNER)
    stdscr.addch(start_y + box_h - 1, start_x + box_w - 1, B_R_CORNER)
    
    stdscr.addstr(start_y + 1, start_x + (box_w - len("GAME OVER")) // 2, "GAME OVER", curses.A_BOLD)
    stdscr.addstr(start_y + 3, start_x + (box_w - len("Press any key to return")) // 2, "Press any key to return")
    stdscr.addstr(start_y + 4, start_x + (box_w - len("to the main menu...")) // 2, "to the main menu...")
    stdscr.refresh()
    self = stdscr.getch()

def main(stdscr, arguments):
    try:
        setup_curses(stdscr)
        menu = MenuController(stdscr, arguments)
        while True:
            settings = menu.navigate()
            if settings is None:
                break
            
            configure_game(settings)
            
            w, h = settings["width"], settings["height"]
            min_width = w * 2 + 35
            min_height = h + 8
            
            screen_height, screen_width = stdscr.getmaxyx()
            if screen_width < min_width or screen_height < min_height:
                stdscr.clear()
                stdscr.addstr(screen_height // 2, max(0, (screen_width - 40) // 2), "Screen configuration is too small!")
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                continue
            
            sub_win = stdscr.derwin(min_height, min_width, (screen_height - min_height) // 2, (screen_width - min_width) // 2)
            sub_win.keypad(True)
            sub_win.nodelay(True)
            
            stdscr.clear()
            stdscr.refresh()
            
            result = game_loop(sub_win, settings["piece"], settings["speed"], w, h, settings["no_color"],
                               mode=settings["mode"], shadow=settings["shadow"], ghost=settings["ghost"])
            
            if result == "MENU":
                continue
                
            show_game_over(stdscr)
            
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e
    finally:
        teardown_curses(stdscr)

if __name__ == "__main__":
    try:
        args = parse_arguments()
        curses.wrapper(main, args)
    except KeyboardInterrupt:
        logger.info("Game interrupted by user (Ctrl+C)")
