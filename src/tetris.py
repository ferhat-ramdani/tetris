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
from constants import COLS, ROWS, MARGIN, DEFAULT_PIECES_FOLDER, DEFAULT_LOG_DIR, DEFAULT_LOG_FIL, COLORS, \
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT, HORIZONTAL_BORDER, VERTICAL_BORDER, T_L_CORNER, T_R_CORNER, \
    B_L_CORNER, B_R_CORNER

logger = logging.getLogger(__name__)

def game_loop(window: curses.window,
              pieces_folder: str,
              speed: str,
              width: int,
              height: int,
              no_color: bool = False
              ):
    """The main game loop that runs until the game is over."""
    colored_pieces = read_pieces(pieces_folder, no_color)
    grid = Grid(height, width)
    gui = GameWindow(window, 14, speed)
    current_colored_piece = clone_piece(random.choice(colored_pieces))
    logger.info("Generated piece %s", current_colored_piece)

    while True:
        position = list((0, width // 2 - 1))
        next_colored_piece = clone_piece(random.choice(colored_pieces))
        logger.info("Generated next piece %s", next_colored_piece)
        can_move_piece = grid.can_move(current_colored_piece, tuple(position), 'd')

        if not can_move_piece:
            logger.info("No more moves available, game over")
            break

        while can_move_piece:
            grid.put_piece(current_colored_piece, tuple(position))
            gui.update_window(grid.matrix, next_colored_piece)

            current_colored_piece = gui.handle_key_events(position, current_colored_piece, next_colored_piece, grid)
            can_move_piece = grid.can_move(current_colored_piece, tuple(position), 'd')
            if can_move_piece:
                grid.remove_piece(current_colored_piece.piece, tuple(position))
                position[0] += 1

        grid.matrix, cleared_lines = grid.clear_filled_lines()

        if cleared_lines > 0:
            can_move_piece = False
            gui.score += cleared_lines
            gui.cleared_lines += cleared_lines
            gui.speed += 1
            logger.info("Score updated to %s", gui.score)
            gui.update_window(grid.matrix, next_colored_piece)

        gui.clear_piece(next_colored_piece, (10, height // 2))
        current_colored_piece = next_colored_piece

def setup_curses(stdscr: curses.window):
    """Setup the curses environment."""
    curses.start_color()
    for color_name, pair_number in COLORS.items():
        curses.init_pair(pair_number, getattr(curses, f"COLOR_{color_name.upper()}"),
                         curses.COLOR_BLACK)
    stdscr.clear()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

def teardown_curses(stdscr: curses.window):
    """Teardown the curses environment."""
    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)

def configure_game(settings: dict):
    """Configure logging and seed based on the active settings."""
    if not os.path.exists(DEFAULT_LOG_DIR):
        os.makedirs(DEFAULT_LOG_DIR)
    
    # Configure logging
    log_file = settings["log"]
    if log_file:
        if not os.path.isabs(log_file):
            log_path = os.path.join(DEFAULT_LOG_DIR, log_file)
        else:
            log_path = log_file
    else:
        log_path = DEFAULT_LOG_FIL
        
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(filename=log_path, level=logging.INFO, filemode='w')
    
    # Seed
    seed = generate_seed()
    random.seed(settings["seed"] if settings["seed"] is not None else seed)
    logger.info("Seed set by %s",
                f"user is {settings['seed']}" if settings["seed"] is not None else f"system is {seed}")

def read_text_input(window: curses.window, y: int, x: int, current_val: str, max_len: int = 20) -> str:
    """Read a string input from the user in curses."""
    curses.curs_set(1)
    curses.echo()
    window.addstr(y, x, " " * (max_len + 4))
    window.move(y, x)
    val = window.getstr(y, x, max_len).decode('utf-8').strip()
    curses.curs_set(0)
    curses.noecho()
    return val

def run_menu(stdscr: curses.window, arguments) -> dict:
    """Run the main start menu. Returns a dictionary of configured settings."""
    settings = {
        "speed": arguments.speed if arguments.speed else "medium",
        "width": arguments.width if arguments.width else COLS,
        "height": arguments.height if arguments.height else ROWS,
        "no_color": arguments.no_color,
        "seed": arguments.seed,
        "piece": arguments.piece if arguments.piece else DEFAULT_PIECES_FOLDER,
        "log": arguments.log
    }

    current_menu = "main"
    selected_idx = 0

    main_options = [
        "Start Game (Default Options)",
        "Advanced Options"
    ]

    adv_keys = ["speed", "width", "height", "no_color", "start", "back"]
    adv_labels = [
        "Speed",
        "Width",
        "Height",
        "Disable Colors",
        "Start Game",
        "Back"
    ]

    stdscr.nodelay(False)
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        menu_min_w = 54
        menu_min_h = 13
        if w < menu_min_w or h < menu_min_h:
            stdscr.addstr(h // 2, max(0, (w - 22) // 2), "Screen is too small!")
            stdscr.addstr(h // 2 + 1, max(0, (w - 38) // 2), f"Please resize to at least {menu_min_w}x{menu_min_h}")
            stdscr.refresh()
            stdscr.getch()
            continue

        box_w = 52
        box_h = 11 if current_menu == "main" else 12
        start_y = (h - box_h) // 2
        start_x = (w - box_w) // 2

        for x_coord in range(start_x, start_x + box_w):
            stdscr.addch(start_y, x_coord, HORIZONTAL_BORDER)
            stdscr.addch(start_y + box_h - 1, x_coord, HORIZONTAL_BORDER)
        for y_coord in range(start_y, start_y + box_h):
            stdscr.addch(y_coord, start_x, VERTICAL_BORDER)
            stdscr.addch(y_coord, start_x + box_w - 1, VERTICAL_BORDER)
        stdscr.addch(start_y, start_x, T_L_CORNER)
        stdscr.addch(start_y, start_x + box_w - 1, T_R_CORNER)
        stdscr.addch(start_y + box_h - 1, start_x, B_L_CORNER)
        stdscr.addch(start_y + box_h - 1, start_x + box_w - 1, B_R_CORNER)

        title = " TERMTRIS "
        stdscr.addstr(start_y, start_x + (box_w - len(title)) // 2, title, curses.A_BOLD)

        if current_menu == "main":
            for idx, opt in enumerate(main_options):
                y_pos = start_y + 3 + idx * 2
                x_pos = start_x + 6
                if idx == selected_idx:
                    stdscr.addstr(y_pos, x_pos, f"> {opt}", curses.A_REVERSE | curses.A_BOLD)
                else:
                    stdscr.addstr(y_pos, x_pos, f"  {opt}")
            
            help_str = "Use UP/DOWN to navigate, ENTER to select"
            stdscr.addstr(start_y + box_h - 2, start_x + (box_w - len(help_str)) // 2, help_str, curses.A_DIM)

        elif current_menu == "advanced":
            h_curr, w_curr = stdscr.getmaxyx()
            max_width_val = w_curr // 2 - 2 - 14
            max_height_val = h_curr - 2
            
            if settings["width"] > max_width_val:
                settings["width"] = max(MIN_WIDTH, max_width_val)
            if settings["height"] > max_height_val:
                settings["height"] = max(MIN_HEIGHT, max_height_val)

            for idx, key in enumerate(adv_keys):
                y_pos = start_y + 2 + idx
                x_pos = start_x + 4
                
                style = curses.A_REVERSE | curses.A_BOLD if idx == selected_idx else curses.A_NORMAL
                
                if key in ["start", "back"]:
                    label = f"[ {adv_labels[idx]} ]"
                    stdscr.addstr(y_pos, start_x + (box_w - len(label)) // 2, label, style)
                else:
                    label = adv_labels[idx] + ":"
                    val = settings[key]
                    if val is None:
                        val_str = "None"
                    elif key == "no_color":
                        val_str = "Disabled" if val else "Enabled"
                    else:
                        val_str = str(val)
                    
                    option_line = f"  {label:<18} [ {val_str} ]"
                    if idx == selected_idx:
                        stdscr.addstr(y_pos, x_pos, option_line, style)
                    else:
                        stdscr.addstr(y_pos, x_pos, option_line)

            help_str = "LEFT/RIGHT to adjust, ENTER to edit/select"
            stdscr.addstr(start_y + box_h - 2, start_x + (box_w - len(help_str)) // 2, help_str, curses.A_DIM)

        stdscr.refresh()

        key = stdscr.getch()
        
        if current_menu == "main":
            if key == curses.KEY_UP:
                selected_idx = (selected_idx - 1) % len(main_options)
            elif key == curses.KEY_DOWN:
                selected_idx = (selected_idx + 1) % len(main_options)
            elif key in [10, 13]:
                if selected_idx == 0:
                    return settings
                elif selected_idx == 1:
                    current_menu = "advanced"
                    selected_idx = 0
        
        elif current_menu == "advanced":
            h_curr, w_curr = stdscr.getmaxyx()
            max_width_val = w_curr // 2 - 2 - 14
            max_height_val = h_curr - 2

            if key == curses.KEY_UP:
                selected_idx = (selected_idx - 1) % len(adv_keys)
            elif key == curses.KEY_DOWN:
                selected_idx = (selected_idx + 1) % len(adv_keys)
            
            else:
                current_key = adv_keys[selected_idx]
                if current_key == "speed":
                    speeds_list = ["slow", "medium", "fast"]
                    curr_speed_idx = speeds_list.index(settings["speed"])
                    if key == curses.KEY_LEFT:
                        settings["speed"] = speeds_list[(curr_speed_idx - 1) % 3]
                    elif key == curses.KEY_RIGHT:
                        settings["speed"] = speeds_list[(curr_speed_idx + 1) % 3]
                
                elif current_key == "width":
                    if key == curses.KEY_LEFT:
                        settings["width"] = max(MIN_WIDTH, settings["width"] - 1)
                    elif key == curses.KEY_RIGHT:
                        settings["width"] = min(max_width_val, settings["width"] + 1)
                
                elif current_key == "height":
                    if key == curses.KEY_LEFT:
                        settings["height"] = max(MIN_HEIGHT, settings["height"] - 1)
                    elif key == curses.KEY_RIGHT:
                        settings["height"] = min(max_height_val, settings["height"] + 1)
                
                elif current_key == "no_color":
                    if key in [curses.KEY_LEFT, curses.KEY_RIGHT, 10, 13]:
                        settings["no_color"] = not settings["no_color"]
                
                elif current_key == "start":
                    if key in [10, 13]:
                        return settings
                
                elif current_key == "back":
                    if key in [10, 13]:
                        current_menu = "main"
                        selected_idx = 1

def show_game_over(stdscr: curses.window):
    """Show the game over message and wait for a keypress."""
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
    
    msg = "GAME OVER"
    msg2 = "Press any key to return"
    msg3 = "to the main menu..."
    stdscr.addstr(start_y + 1, start_x + (box_w - len(msg)) // 2, msg, curses.A_BOLD)
    stdscr.addstr(start_y + 3, start_x + (box_w - len(msg2)) // 2, msg2)
    stdscr.addstr(start_y + 4, start_x + (box_w - len(msg3)) // 2, msg3)
    stdscr.refresh()
    stdscr.getch()

def main(stdscr: curses.window, arguments):
    """The main function that initializes the game."""
    try:
        setup_curses(stdscr)
        while True:
            settings = run_menu(stdscr, arguments)
            if settings is None:
                break
            
            configure_game(settings)
            
            w = settings["width"]
            h = settings["height"]
            min_width = w * 2 + 35
            min_height = h + 2
            
            screen_height, screen_width = stdscr.getmaxyx()
            if screen_width < min_width or screen_height < min_height:
                stdscr.clear()
                msg = "Screen is too small for this configuration!"
                msg2 = f"Required: {min_width}x{min_height}, Available: {screen_width}x{screen_height}"
                msg3 = "Press any key to return to menu..."
                stdscr.addstr(screen_height // 2 - 1, max(0, (screen_width - len(msg)) // 2), msg, curses.A_BOLD)
                stdscr.addstr(screen_height // 2, max(0, (screen_width - len(msg2)) // 2), msg2)
                stdscr.addstr(screen_height // 2 + 1, max(0, (screen_width - len(msg3)) // 2), msg3)
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                continue
            
            start_y = (screen_height - min_height) // 2
            start_x = (screen_width - min_width) // 2
            sub_win = stdscr.derwin(min_height, min_width, start_y, start_x)
            sub_win.keypad(True)
            sub_win.nodelay(True)
            
            stdscr.clear()
            stdscr.refresh()
            
            game_loop(sub_win, settings["piece"], settings["speed"], w, h, settings["no_color"])
            
            show_game_over(stdscr)
            
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e
    finally:
        teardown_curses(stdscr)
        print("trying here")

try:
    args = parse_arguments()
    curses.wrapper(main, args)
except KeyboardInterrupt:
    logger.info("Game interrupted by user (Ctrl+C)")
    print("Game interrupted by user (Ctrl+C)")

