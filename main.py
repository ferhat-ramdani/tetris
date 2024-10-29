import curses
import random

from pieces import *
from gui import *
from grid import *

COLS = 10
ROWS = 10

MARGIN = 20
start_pos = (0, COLS // 2 - 1)

window: curses.window = curses.initscr()

def game_loop():
	pieces = read_pieces('pieces')
	grid = Grid(ROWS, COLS)
	gui = GameWindow(window, MARGIN)
	current_piece = random.choice(pieces)

	while(True):
		position = list(start_pos)
		next_piece = random.choice(pieces)
		gui.update_window(grid.matrix, next_piece)
		can_move_piece = can_move_piece = grid.can_move(current_piece, tuple(position), 'b')

		if(not can_move_piece):
			break

		while can_move_piece:
			grid.put_piece(current_piece, tuple(position))
			grid.matrix, cleared_lines = grid.clear_filled_lines()
			gui.update_window(grid.matrix, next_piece)
			window.refresh()

			if cleared_lines > 0:
				can_move_piece = False
				gui.score += cleared_lines
				continue

			current_piece = gui.handle_key_events(position, current_piece, next_piece, grid)
			
			can_move_piece = grid.can_move(current_piece, tuple(position), 'b')
			if can_move_piece:
				grid.remove_piece(current_piece, tuple(position))
				position[0] += 1
				window.clear()

		gui.clear_piece(next_piece, (10, ROWS // 2))
		current_piece = next_piece


def main(window: curses.window):
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