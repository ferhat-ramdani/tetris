import curses
import random

from pieces import *
from gui import *
from grid import *

COLS = 15
ROWS = 10

MARGIN = 20
start_pos = (0, COLS // 2 - 1)

window: curses.window = curses.initscr()

def game_loop():
	pieces = read_pieces('pieces')
	grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
	current_piece = random.choice(pieces)

	while(True):
		position = list(start_pos)
		next_piece = random.choice(pieces)
		update_window(window, grid, next_piece, MARGIN)
		can_move_piece = can_move_piece = can_move(grid, current_piece, tuple(position), 'b')

		if(not can_move_piece):
			break

		while can_move_piece:
			put_piece(grid, current_piece, tuple(position))
			grid, cleared_lines = clear_filled_lines(grid)
			update_window(window, grid, next_piece, MARGIN)
			window.refresh()

			if cleared_lines > 0:
				can_move_piece = False
				continue

			current_piece = handle_key_events(window, position, current_piece, next_piece, grid, MARGIN)
			
			can_move_piece = can_move(grid, current_piece, tuple(position), 'b')
			if can_move_piece:
				remove_piece(grid, current_piece, tuple(position))
				position[0] += 1
				window.clear()

		clear_piece(window, next_piece, 10, ROWS // 2)
		current_piece = next_piece


def main(window):
	curses.curs_set(0)
	curses.noecho()
	curses.cbreak()
	window.keypad(True)
	window.nodelay(True)

	game_loop()

	curses.curs_set(1)
	curses.echo()
	curses.nocbreak()
	window.keypad(False)

curses.wrapper(main)