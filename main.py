import curses
import random

from pieces import *
from gui import *
from grid import *

COLS = 15
ROWS = 10

start_pos = (0, COLS // 2 - 1)

stdscr: curses.window = curses.initscr()

def game_loop():
	pieces = read_pieces('pieces')
	grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

	while(True):
		position = list(start_pos)
		random_piece = random.choice(pieces)
		can_move_piece = True

		while can_move_piece:
			put_piece(grid, random_piece, tuple(position))
			grid, cleared_lines = clear_filled_lines(grid)
			draw_borders(stdscr, COLS, ROWS)
			draw_grid(stdscr, grid)
			stdscr.refresh()

			if cleared_lines > 0:
				can_move_piece = False
				continue

			random_piece = handle_key_events(stdscr, position, random_piece, grid, COLS, ROWS)
			
			can_move_piece = can_move(grid, random_piece, tuple(position), 'b')
			if can_move_piece:
				remove_piece(grid, random_piece, tuple(position))
				position[0] += 1
				stdscr.clear()


def main(stdscr):
	curses.curs_set(0)
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)
	stdscr.nodelay(True)

	game_loop()

	curses.curs_set(1)
	curses.echo()
	curses.nocbreak()
	stdscr.keypad(False)

curses.wrapper(main)